"""
Módulo do Sistema Especialista com Encadeamento para Trás (Backward Chaining)
e Geração de Explicação Estruturada para o Projeto Caatinga.AI.

Atende às Seções 4.1, 4.2 e 4.4 da Sprint 1:
  - 4.1: Mini sistema especialista com regras SE ... ENTÃO ... para manejo de talhão,
         motor retroativo e resposta estruturada ao "Por que você concluiu isso?".
  - 4.2: Quebra da base inicial com caso legítimo do domínio da fruticultura
         (período de carência pré-colheita na manga) e regra corretiva sem contradições.
  - 4.4: Regra explícita de salvaguarda agronômica e responsabilidade sanitária.
"""

import os
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

# Garante que a raiz do repositório esteja no sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class Regra:
    """
    Representação de uma regra de produção SE <antecedentes> ENTÃO <consequente>.
    """
    def __init__(self, id_regra: str, antecedentes: List[str], consequente: str, descricao: str = ""):
        self.id_regra = id_regra
        self.antecedentes = [ant.strip() for ant in antecedentes]
        self.consequente = consequente.strip()
        self.descricao = descricao

    def __repr__(self) -> str:
        premissas_str = " E ".join(self.antecedentes)
        return f"[{self.id_regra}] SE {premissas_str} ENTÃO {self.consequente}"


class NoExplicacao:
    """Nó da árvore de explicação para rastreamento da inferência retroativa."""
    def __init__(self, objetivo: str, regra_usada: Optional[Regra] = None, tipo: str = "derivado"):
        self.objetivo = objetivo
        self.regra_usada = regra_usada
        self.tipo = tipo  # 'fato_inicial' ou 'derivado'
        self.subexplicacoes: List['NoExplicacao'] = []

    def formatar_cadeia(self, nivel: int = 0) -> List[str]:
        """Gera a árvore explicativa identada para visualização humana."""
        linhas = []
        indent = "    " * nivel
        marcador = "|-- " if nivel > 0 else ""

        if self.tipo == "fato_inicial":
            linhas.append(f"{indent}{marcador}Fato comprovado da base sensorial: '{self.objetivo}'")
        else:
            linhas.append(f"{indent}{marcador}Conclusão: '{self.objetivo}'")
            if self.regra_usada:
                linhas.append(f"{indent}    Disparou {self.regra_usada}")
                if self.regra_usada.descricao:
                    linhas.append(f"{indent}    Justificativa técnica: {self.regra_usada.descricao}")
            for sub in self.subexplicacoes:
                linhas.extend(sub.formatar_cadeia(nivel + 1))
        return linhas


class MotorInferenciaRetroativo:
    """
    Motor de inferência que aplica Encadeamento para Trás (Backward Chaining)
    a partir de um objetivo (hipótese), rastreando passo a passo as regras acionadas.
    """
    def __init__(self, regras: List[Regra]):
        self.regras = regras

    def provar_objetivo(self,
                        objetivo: str,
                        fatos: Set[str],
                        caminho_pilha: Optional[Set[str]] = None) -> Tuple[bool, Optional[NoExplicacao]]:
        """
        Tenta provar recursivamente o objetivo com encadeamento para trás.
        Retorna (sucesso: bool, arvore_explicacao: NoExplicacao).
        """
        if caminho_pilha is None:
            caminho_pilha = set()

        # Prevenção de loops cíclicos no grafo de regras
        if objetivo in caminho_pilha:
            return False, None

        # Caso base 1: O objetivo já é um fato conhecido
        if objetivo in fatos:
            return True, NoExplicacao(objetivo, None, tipo="fato_inicial")

        caminho_pilha.add(objetivo)

        # Busca regras cujo consequente satisfaz o objetivo
        regras_candidatas = [r for r in self.regras if r.consequente == objetivo]

        for regra in regras_candidatas:
            todas_premissas_ok = True
            sub_arvores = []

            for premissa in regra.antecedentes:
                ok, sub_arvore = self.provar_objetivo(premissa, fatos, caminho_pilha)
                if not ok:
                    todas_premissas_ok = False
                    break
                sub_arvores.append(sub_arvore)

            if todas_premissas_ok:
                no = NoExplicacao(objetivo, regra, tipo="derivado")
                no.subexplicacoes = sub_arvores
                caminho_pilha.remove(objetivo)
                return True, no

        caminho_pilha.remove(objetivo)
        return False, None


# --- Definição das Bases de Regras (Domínio: Manga no Vale do São Francisco) ---

def obter_base_regras_inicial() -> List[Regra]:
    """
    Base Inicial (v1 - 6 regras) antes da quebra da base.
    Focada em sintomas diretos de pragas, irrigação e tempo de pulverização.
    """
    return [
        Regra(
            id_regra="R1",
            antecedentes=["armadilha_positiva", "solo_encharcado", "dias_desde_pulverizacao_maior_14"],
            consequente="risco_fitossanitario_alto",
            descricao="Solo encharcado acumulado a longo período sem pulverização com captura óptica ativa pragas."
        ),
        Regra(
            id_regra="R2",
            antecedentes=["risco_fitossanitario_alto", "em_frutificacao"],
            consequente="inspecionar_prioridade_alta",
            descricao="Fase de frutificação vulnerável a danos de polpa por mosca-das-frutas."
        ),
        Regra(
            id_regra="R3",
            antecedentes=["inspecionar_prioridade_alta", "alta_densidade_pragas"],
            consequente="aplicar_defensivo_quimico_emergencial",
            descricao="Infestação severa confirmada demanda aplicação imediata de defensivo químico de choque."
        ),
        Regra(
            id_regra="R4",
            antecedentes=["armadilha_positiva", "solo_firme", "dias_desde_pulverizacao_menor_igual_14"],
            consequente="monitorar_armadilha_48h",
            descricao="Risco controlado em solo firme dentro do período de proteção residual; recomenda-se monitorar."
        ),
        Regra(
            id_regra="R5",
            antecedentes=["armadilha_negativa", "solo_firme"],
            consequente="manter_rotina_preventiva",
            descricao="Talhão estável sem indício de praga na armadilha em terreno seco."
        ),
        Regra(
            id_regra="R6",
            antecedentes=["manter_rotina_preventiva", "dias_para_colheita_menor_igual_7"],
            consequente="liberar_talhao_para_colheita",
            descricao="Talhão sadio e seguro para colheita dentro da janela final da safra."
        )
    ]


def obter_base_regras_corrigida() -> List[Regra]:
    """
    Base Corrigida (v2 - 7 regras).
    Incorpora salvaguarda agronômica e período de carência (Seção 4.2 e 4.4).
    Evita contaminação de mangas prontas para consumo humano / exportação.
    """
    return [
        Regra(
            id_regra="R1",
            antecedentes=["armadilha_positiva", "solo_encharcado", "dias_desde_pulverizacao_maior_14"],
            consequente="risco_fitossanitario_alto",
            descricao="Solo encharcado acumulado a longo período sem pulverização com captura óptica ativa pragas."
        ),
        Regra(
            id_regra="R2",
            antecedentes=["risco_fitossanitario_alto", "em_frutificacao"],
            consequente="inspecionar_prioridade_alta",
            descricao="Fase de frutificação vulnerável a danos de polpa por mosca-das-frutas."
        ),
        Regra(
            id_regra="R3",
            antecedentes=["inspecionar_prioridade_alta", "alta_densidade_pragas", "periodo_carencia_seguro"],
            consequente="aplicar_defensivo_quimico_emergencial",
            descricao="Aplicação química autorizada apenas se o período de carência for respeitado até a colheita."
        ),
        Regra(
            id_regra="R4",
            antecedentes=["armadilha_positiva", "solo_firme", "dias_desde_pulverizacao_menor_igual_14"],
            consequente="monitorar_armadilha_48h",
            descricao="Risco controlado em solo firme dentro do período de proteção residual; recomenda-se monitorar."
        ),
        Regra(
            id_regra="R5",
            antecedentes=["armadilha_negativa", "solo_firme"],
            consequente="manter_rotina_preventiva",
            descricao="Talhão estável sem indício de praga na armadilha em terreno seco."
        ),
        Regra(
            id_regra="R6",
            antecedentes=["manter_rotina_preventiva", "dias_para_colheita_menor_igual_7"],
            consequente="liberar_talhao_para_colheita",
            descricao="Talhão sadio e seguro para colheita dentro da janela final da safra."
        ),
        Regra(
            id_regra="R7_SALVAGUARDA",
            antecedentes=["inspecionar_prioridade_alta", "alta_densidade_pragas", "colheita_iminente_sob_carencia"],
            consequente="aplicar_controle_biologico_e_interditar_colheita",
            descricao="Salvaguarda Sanitária: colheita em menos de 7 dias proíbe defensivos químicos por lei sanitária; "
                      "exige controle biológico de choque e interdição preventiva do lote."
        )
    ]


# --- Demonstração e Traço de Execução ---

def executar_caso_estudo_quebra_base() -> Dict[str, Any]:
    """
    Demonstra o caso da Seção 4.2:
      Cenário: Talhão com alta infestação em frutificação a 3 dias da colheita (período de carência violado).
      Antes (Base Inicial): Recomenda pulverização química, gerando contaminação ilegal de alimentos.
      Depois (Base Corrigida): Bloqueia o químico e aciona controle biológico + interdição sanitária.
    """
    # Fatos presentes no talhão crítico avaliado
    fatos_cenario_critico = {
        "armadilha_positiva",
        "solo_encharcado",
        "dias_desde_pulverizacao_maior_14",
        "em_frutificacao",
        "alta_densidade_pragas",
        "colheita_iminente_sob_carencia"  # Falta apenas 3 dias para colheita; carência mínima é de 14 dias
    }

    # Execução na Base Inicial (v1)
    motor_v1 = MotorInferenciaRetroativo(obter_base_regras_inicial())
    sucesso_v1_quimico, arvore_v1_quimico = motor_v1.provar_objetivo(
        "aplicar_defensivo_quimico_emergencial",
        fatos_cenario_critico
    )

    # Execução na Base Corrigida (v2)
    motor_v2 = MotorInferenciaRetroativo(obter_base_regras_corrigida())
    sucesso_v2_quimico, arvore_v2_quimico = motor_v2.provar_objetivo(
        "aplicar_defensivo_quimico_emergencial",
        fatos_cenario_critico
    )
    sucesso_v2_biologico, arvore_v2_biologico = motor_v2.provar_objetivo(
        "aplicar_controle_biologico_e_interditar_colheita",
        fatos_cenario_critico
    )

    return {
        "fatos": fatos_cenario_critico,
        "v1_quimico_provado": sucesso_v1_quimico,
        "arvore_v1_quimico": arvore_v1_quimico,
        "v2_quimico_provado": sucesso_v2_quimico,
        "arvore_v2_quimico": arvore_v2_quimico,
        "v2_biologico_provado": sucesso_v2_biologico,
        "arvore_v2_biologico": arvore_v2_biologico,
    }


def imprimir_relatorio_especialista():
    """Imprime no terminal o relatório formatado do sistema especialista."""
    print("=" * 80)
    print("SISTEMA ESPECIALISTA FITOSSANITÁRIO - CAATINGA.AI (VALE DO SÃO FRANCISCO)")
    print("Mecanismo de Raciocínio: Encadeamento para Trás (Backward Chaining)")
    print("=" * 80)

    resultado = executar_caso_estudo_quebra_base()

    print("\n--- 1. FATOS OBSERVADOS NO TALHÃO DE TESTE ---")
    for f in sorted(resultado["fatos"]):
        print(f"  * {f}")

    print("\n--- 2. TRAÇO ANTES: BASE INICIAL (v1 - Falha Crítica de Carência) ---")
    print(f"Tentativa de provar: 'aplicar_defensivo_quimico_emergencial' -> {resultado['v1_quimico_provado']}")
    if resultado["arvore_v1_quimico"]:
        print("Cadeia explicativa da conclusão ('Por que você concluiu isso?'):")
        for linha in resultado["arvore_v1_quimico"].formatar_cadeia():
            print(f"  {linha}")
    print("\nAVALIAÇÃO DE RISCO: A recomendação da base v1 geraria violação grave da ANVISA/MAPA,")
    print("pois pulveriza químico em mangas a 3 dias da colheita (carencia mínima de 14 dias).")

    print("\n" + "-" * 80)
    print("--- 3. TRAÇO DEPOIS: BASE CORRIGIDA (v2 - Com Salvaguarda Sanitária R7) ---")
    print(f"1) Provar 'aplicar_defensivo_quimico_emergencial' -> {resultado['v2_quimico_provado']}")
    print("   Resultado: BLOQUEADO (a premissa 'periodo_carencia_seguro' não foi satisfeita).")

    print(f"\n2) Provar 'aplicar_controle_biologico_e_interditar_colheita' -> {resultado['v2_biologico_provado']}")
    if resultado["arvore_v2_biologico"]:
        print("Cadeia explicativa da conclusão ('Por que você concluiu isso?'):")
        for linha in resultado["arvore_v2_biologico"].formatar_cadeia():
            print(f"  {linha}")

    print("\n" + "=" * 80)
    print("DIAGNÓSTICO FINAL: A base corrigida evitou contaminação tóxica e preservou a safra.")
    print("=" * 80)


if __name__ == "__main__":
    imprimir_relatorio_especialista()
