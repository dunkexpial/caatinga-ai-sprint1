"""
Módulo do Contraexemplo Bônus da Liga de IA (+0,3 ponto).
Projeto Caatinga.AI - Sprint 1 (Seção Bônus - Liga de IA do enunciado).
Autor: João Vítor Almeida dos Santos (Commit 8)

Enunciado do Bônus:
  "Construa à mão um pomar de no máximo 8 × 8 em que a sua DFS (com a ordem de vizinhos
   que você declarou) devolva uma rota com custo maior que o dobro do ótimo.
   Entregue a grade, a rota devolvida, a rota ótima e os dois custos.
   O ponto é pela construção do contraexemplo, não pela sorte."

Diretriz Técnica da Dupla:
  Ordem estrita de expansão de vizinhos (De Sul a Norte):
    1. Sul:   (+1,  0)
    2. Leste: ( 0, +1)
    3. Oeste: ( 0, -1)
    4. Norte: (-1,  0)
"""

import os
import sys
from typing import Any, Dict, List, Tuple

# Garante que a raiz do repositório esteja no sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from src.gerador_pomar import BLOQUEADO, CUSTO
    from src.buscas import busca_custo_uniforme, busca_profundidade
except ImportError:
    from gerador_pomar import BLOQUEADO, CUSTO
    from buscas import busca_custo_uniforme, busca_profundidade


# ==============================================================================
# Grade 8x8 Construída à Mão (Design Arquitetural do Contraexemplo)
# ==============================================================================
# Dimensão: 8x8 (atende ao requisito de no máximo 8x8)
# Ponto de Partida (Portão): (0, 0)
# Ponto de Coleta (Objetivo): (7, 7)
#
# Arquitetura dos Corredores:
#   - Rota Norte/Leste (Ótima - Descoberta pelo UCS):
#     Avança pela linha 0 de (0,0) a (0,7) e desce pela coluna 7 de (0,7) a (7,7).
#     Composta 100% por carreadores firmes ('.', custo 1).
#     Passos: 14 | Custo: 14 * 1 = 14.
#
#   - Rota Sul/Oeste (Armadilha de Alta Prioridade - Capturada pelo DFS):
#     No início (0,0), a ordem de vizinhos prioriza Sul (+1, 0) sobre Leste (0, +1).
#     O DFS é atraído para o Sul e avança pela coluna 0 até (7,0), virando a Leste
#     pela linha 7 até (7,7).
#     Composta por 13 células de solo encharcado ('~', custo 4) e 1 de carreador final (7,7).
#     Passos: 14 | Custo: (13 * 4) + (1 * 1) = 52 + 1 = 53.
#
#   - Miolo Central (Linhas 1 a 6, Colunas 1 a 6):
#     Preenchido com obstáculos intransitáveis ('#') para canalizar deterministicamente
#     as escolhas e isolar os dois corredores.
#
# Relação Matemática:
#   Custo DFS = 53
#   Custo UCS (Ótimo) = 14
#   Dobro do Ótimo = 2 * 14 = 28
#   53 > 28 => Custo DFS é 3,79 vezes maior que o ótimo (quase o quádruplo)!
# ==============================================================================

GRADE_CONTRAEXEMPLO: List[List[str]] = [
    [".", ".", ".", ".", ".", ".", ".", "."],  # Linha 0: Rodovia de Carreadores ('.')
    ["~", "#", "#", "#", "#", "#", "#", "."],  # Linhas 1-6: Parede de Bloqueios ('#')
    ["~", "#", "#", "#", "#", "#", "#", "."],  # isolando a vala de lama ('~') à esquerda
    ["~", "#", "#", "#", "#", "#", "#", "."],  # do carreador limpo ('.') à direita
    ["~", "#", "#", "#", "#", "#", "#", "."],
    ["~", "#", "#", "#", "#", "#", "#", "."],
    ["~", "#", "#", "#", "#", "#", "#", "."],
    ["~", "~", "~", "~", "~", "~", "~", "."],  # Linha 7: Vala de lama ('~') até (7,7)
]


def formatar_grade(grade: List[List[str]],
                   caminho_destaque: List[Tuple[int, int]] = None,
                   simbolo_marcador: str = "*") -> List[str]:
    """Formata visualmente a grade com índices de linhas e colunas."""
    n = len(grade)
    caminho_set = set(caminho_destaque) if caminho_destaque else set()
    linhas = []

    cabecalho = "     " + " ".join(f"{c:2d}" for c in range(n))
    linhas.append(cabecalho)
    linhas.append("    " + "-" * (n * 3 + 1))

    for r in range(n):
        celulas = []
        for c in range(n):
            if (r, c) == (0, 0):
                celulas.append(" S")  # Start
            elif (r, c) == (n - 1, n - 1):
                celulas.append(" G")  # Goal
            elif (r, c) in caminho_set:
                celulas.append(f" {simbolo_marcador}")
            else:
                celulas.append(f" {grade[r][c]}")
        linhas.append(f"{r:2d} |" + "".join(celulas))
    return linhas


def executar_contraexemplo() -> Dict[str, Any]:
    """
    Executa a validação formal do contraexemplo, calculando a rota DFS e UCS,
    seus custos exatos e a comprovação matemática do bônus.
    """
    inicio = (0, 0)
    objetivo = (7, 7)

    # Executa Busca em Profundidade (DFS)
    res_dfs = busca_profundidade(GRADE_CONTRAEXEMPLO, inicio=inicio, objetivo=objetivo)

    # Executa Busca de Custo Uniforme (UCS - Ótimo em Custo)
    res_ucs = busca_custo_uniforme(GRADE_CONTRAEXEMPLO, inicio=inicio, objetivo=objetivo)

    custo_dfs = res_dfs["custo"]
    custo_ucs = res_ucs["custo"]
    dobro_otimo = 2 * custo_ucs
    razao = custo_dfs / custo_ucs if custo_ucs > 0 else float("inf")
    atingiu_bonus = custo_dfs > dobro_otimo

    return {
        "grade": GRADE_CONTRAEXEMPLO,
        "dimensao": len(GRADE_CONTRAEXEMPLO),
        "inicio": inicio,
        "objetivo": objetivo,
        "dfs": {
            "caminho": res_dfs["caminho"],
            "custo": custo_dfs,
            "passos": res_dfs["passos"],
            "nos_expandidos": res_dfs["nos_expandidos"],
        },
        "ucs": {
            "caminho": res_ucs["caminho"],
            "custo": custo_ucs,
            "passos": res_ucs["passos"],
            "nos_expandidos": res_ucs["nos_expandidos"],
        },
        "dobro_do_otimo": dobro_otimo,
        "razao_dfs_ucs": round(razao, 3),
        "atingiu_bonus": atingiu_bonus,
    }


def imprimir_relatorio_contraexemplo(dados: Dict[str, Any]) -> None:
    """Exibe no terminal o relatório técnico estruturado com o contraexemplo e a dedução teórica."""
    dfs = dados["dfs"]
    ucs = dados["ucs"]

    print("=" * 86)
    print("  BÔNUS - LIGA DE IA (+0,3 PONTO): CONTRAEXEMPLO FORMAL PARA DFS > 2x ÓTIMO")
    print("  Disciplina: Inteligência Artificial - Prof. Ronierison Maciel - UniRios 2026.2")
    print("  Autor: João Vítor Almeida dos Santos (Commit 8)")
    print("=" * 86)

    print("\n[1. GRADE CONSTRUÍDA À MÃO (8x8)]")
    print("Legenda: '.' = Carreador (custo 1) | '~' = Solo Encharcado (custo 4) | '#' = Bloqueio\n")
    for linha in formatar_grade(dados["grade"]):
        print(linha)

    print("\n" + "-" * 86)
    print("[2. RESULTADOS COMPARATIVOS: DFS vs UCS (ÓTIMO)]")
    print("-" * 86)
    print(f"{'Métrica':<30} | {'DFS (Busca em Profundidade)':<27} | {'UCS (Custo Uniforme)':<22}")
    print("-" * 86)
    print(f"{'Custo Total da Rota':<30} | {dfs['custo']:<27} | {ucs['custo']:<22}")
    print(f"{'Número de Passos':<30} | {dfs['passos']:<27} | {ucs['passos']:<22}")
    print(f"{'Nós Expandidos':<30} | {dfs['nos_expandidos']:<27} | {ucs['nos_expandidos']:<22}")
    print("-" * 86)
    print(f"Condição do Bônus: Custo(DFS) > 2 * Custo(Ótimo) => {dfs['custo']} > 2 * {ucs['custo']} ({dados['dobro_do_otimo']})")
    print(f"Razão Custo(DFS) / Custo(Ótimo): {dados['razao_dfs_ucs']}x (quase 4x maior que o ótimo!)")
    print(f"Status da Validação do Bônus: {'[APROVADO - SUCESSO PLENO]' if dados['atingiu_bonus'] else '[REPROVADO]'}")

    print("\n" + "-" * 86)
    print("[3. ROTAS IDENTIFICADAS]")
    print("-" * 86)
    print("Rota Ótima Devolvida pelo UCS (Custo = 14):")
    print(f"  {ucs['caminho']}")
    print("\nRota Subótima Devolvida pelo DFS (Custo = 53):")
    print(f"  {dfs['caminho']}")

    print("\n" + "-" * 86)
    print("[4. JUSTIFICATIVA E DEDUÇÃO TEÓRICA (CONSTRUÇÃO CONCEITUAL, NÃO POR SORTE)]")
    print("-" * 86)
    print(
        "1. Preferência Direcional Fixada (De Sul a Norte):\n"
        "   Nossa ordem de expansão declarada é rigorosamente:\n"
        "     1º Sul (+1, 0) -> 2º Leste (0, +1) -> 3º Oeste (0, -1) -> 4º Norte (-1, 0).\n"
        "   No nó inicial (0, 0), o agente possui dois vizinhos válidos desobstruídos:\n"
        "     - Sul em (1, 0) [terreno encharcado '~']\n"
        "     - Leste em (0, 1) [carreador firme '.']\n\n"
        "2. Armadilha de Profundidade:\n"
        "   Por priorizar o Sul, o DFS empilha Leste e depois Sul, retirando imediatamente (1, 0)\n"
        "   do topo da pilha LIFO. Ao entrar em (1, 0), o DFS avança exclusivamente para o Sul\n"
        "   ao longo de toda a coluna 0 até (7, 0), pois as células à direita (coluna 1) estão\n"
        "   bloqueadas por galpões ('#'). Em (7, 0), sem opção ao Sul, avança para Leste pela\n"
        "   linha 7 até alcançar o objetivo em (7, 7).\n\n"
        "3. Cegueira a Custos de Transição:\n"
        "   O algoritmo DFS é uma busca cega indiferente a custos de arco g(n). Como a rota ao Sul\n"
        "   atinge o objetivo sem beco sem saída (dead-end), o DFS jamais faz backtracking para\n"
        "   avaliar o ramo Leste. Ele conclui a busca e devolve a rota lamacenta com 13 células\n"
        "   encharcadas (13 * 4 = 52) e o talhão final (1 * 1 = 1), perfazendo custo 53.\n\n"
        "4. Ação do UCS:\n"
        "   O UCS expande nós por ordem estrita de custo acumulado g(n) via fila de prioridade.\n"
        "   Ele descobre e percorre a rodovia de carreadores na borda norte (linha 0) e leste\n"
        "   (coluna 7), totalizando 14 passos a custo unitário (custo 14).\n\n"
        "Conclusão: O contraexemplo foi construído com base na topologia do grafo e na ordem de\n"
        "geração dos operadores, comprovando formalmente a perda severa de qualidade de rota que o\n"
        "DFS impõe em ambientes de terreno não uniforme."
    )
    print("=" * 86 + "\n")


if __name__ == "__main__":
    resultado = executar_contraexemplo()
    imprimir_relatorio_contraexemplo(resultado)
