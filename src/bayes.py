"""
Módulo de Análise Bayesiana do Sensor Óptico de Pragas para o Projeto Caatinga.AI.
Atende à Seção 4.3 do enunciado da Sprint 1.

Analisa probabilisticamente a eficácia do sensor óptico nas lavouras do semiárido,
demonstrando formalmente o Teorema de Bayes, a taxa de alertas falsos, o impacto
operacional em horas de agrônomos e o paradoxo da taxa base (sensibilidade vs falso positivo).
"""

import os
import sys
from typing import Dict, Any, Optional

# Garante que a raiz do repositório esteja no sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from src.gerador_pomar import parametros_sensor
except ImportError:
    from gerador_pomar import parametros_sensor


def calcular_probabilidade_posterior(prevalencia: float,
                                     sensibilidade: float,
                                     taxa_falso_positivo: float) -> Dict[str, float]:
    """
    Aplica o Teorema de Bayes para calcular a probabilidade a posteriori de infestação real
    dado que o sensor disparou um alerta positivo: P(Infestado | Sensor+).

    Fórmula:
      P(Infestado | Sensor+) = [P(Sensor+ | Infestado) * P(Infestado)] / P(Sensor+)
      onde P(Sensor+) = P(Sensor+ | Infestado)*P(Infestado) + P(Sensor+ | Saudavel)*P(Saudavel)
    """
    p_infestado = prevalencia
    p_saudavel = 1.0 - prevalencia

    # Verossimilhanças
    p_pos_dado_infestado = sensibilidade
    p_pos_dado_saudavel = taxa_falso_positivo

    # Probabilidade total de teste positivo (Evidência marginal)
    p_sensor_positivo = (p_pos_dado_infestado * p_infestado) + (p_pos_dado_saudavel * p_saudavel)

    # Valor Preditivo Positivo (VPP)
    p_infestado_dado_positivo = (p_pos_dado_infestado * p_infestado) / p_sensor_positivo

    # Taxa de Falsos Alertas (False Discovery Rate - FDR)
    taxa_alertas_falsos = 1.0 - p_infestado_dado_positivo

    return {
        "p_infestado": p_infestado,
        "p_saudavel": p_saudavel,
        "sensibilidade": sensibilidade,
        "taxa_falso_positivo": taxa_falso_positivo,
        "p_sensor_positivo": p_sensor_positivo,
        "vpp": p_infestado_dado_positivo,
        "taxa_alertas_falsos": taxa_alertas_falsos,
    }


def calcular_impacto_campo(prevalencia: float,
                           sensibilidade: float,
                           taxa_falso_positivo: float,
                           talhoes_semana: int,
                           minutos_por_inspecao: float = 12.0) -> Dict[str, float]:
    """
    Calcula as métricas operacionais semanais em campo com base no volume de talhões inspecionados:
      - Total de talhões inspecionados
      - Alertas totais gerados pelo sensor
      - Alertas verdadeiros (talhões infestados detectados)
      - Alertas falsos (talhões saudáveis com alarme falso)
      - Horas semanais de agrônomos desperdiçadas em falsos alertas
      - Horas semanais totais de inspeção motivadas pelo sensor
    """
    bayes = calcular_probabilidade_posterior(prevalencia, sensibilidade, taxa_falso_positivo)

    total_infestados = talhoes_semana * prevalencia
    total_saudaveis = talhoes_semana * (1.0 - prevalencia)

    alertas_verdadeiros = total_infestados * sensibilidade
    alertas_falsos = total_saudaveis * taxa_falso_positivo
    alertas_totais = alertas_verdadeiros + alertas_falsos

    horas_por_inspecao = minutos_por_inspecao / 60.0
    horas_alertas_falsos = alertas_falsos * horas_por_inspecao
    horas_totais_inspecoes = alertas_totais * horas_por_inspecao

    return {
        "talhoes_semana": talhoes_semana,
        "total_infestados": total_infestados,
        "total_saudaveis": total_saudaveis,
        "alertas_totais": alertas_totais,
        "alertas_verdadeiros": alertas_verdadeiros,
        "alertas_falsos": alertas_falsos,
        "horas_alertas_falsos": horas_alertas_falsos,
        "horas_totais_inspecoes": horas_totais_inspecoes,
        "minutos_por_inspecao": minutos_por_inspecao,
        "vpp": bayes["vpp"],
        "taxa_alertas_falsos": bayes["taxa_alertas_falsos"],
    }


def analisar_sensor_bayesiano(matricula: int = 24114066) -> Dict[str, Any]:
    """
    Executa a análise bayesiana completa dos quatro itens (a, b, c, d) da Seção 4.3 do enunciado,
    utilizando os parâmetros oficiais gerados para a matrícula informada.
    """
    params = parametros_sensor(matricula)
    prev = params["prevalencia"]
    sens = params["sensibilidade"]
    fpr = params["taxa_falso_positivo"]
    n_talhoes = params["talhoes_por_semana"]

    # (a) e (b) Probabilidade posterior e taxa de falsos alertas
    res_bayes = calcular_probabilidade_posterior(prev, sens, fpr)

    # (c) Impacto no campo (800 talhões/semana, 12 min/inspeção)
    res_campo = calcular_impacto_campo(prev, sens, fpr, n_talhoes, minutos_por_inspecao=12.0)

    # (d) Cenário de aumento de sensibilidade para 99.9% mantendo falso positivo em 3%
    sens_d = 0.999
    res_cenario_d = calcular_probabilidade_posterior(prev, sens_d, fpr)
    res_campo_d = calcular_impacto_campo(prev, sens_d, fpr, n_talhoes, minutos_por_inspecao=12.0)

    # Frase requerida no item (b)
    percentual_falsos_arredondado = round(res_bayes["taxa_alertas_falsos"] * 100)
    frase_oficial = f"a cada 100 alertas do meu sistema, cerca de {percentual_falsos_arredondado} serao falsos."

    return {
        "matricula": matricula,
        "parametros": params,
        "item_a": {
            "p_infestado": prev,
            "sensibilidade": sens,
            "taxa_falso_positivo": fpr,
            "p_sensor_positivo": res_bayes["p_sensor_positivo"],
            "vpp": res_bayes["vpp"],
            "vpp_percentual": round(res_bayes["vpp"] * 100, 2),
        },
        "item_b": {
            "taxa_alertas_falsos": res_bayes["taxa_alertas_falsos"],
            "taxa_alertas_falsos_percentual": round(res_bayes["taxa_alertas_falsos"] * 100, 2),
            "frase_completada": frase_oficial,
        },
        "item_c": {
            "talhoes_por_semana": n_talhoes,
            "alertas_totais": round(res_campo["alertas_totais"], 3),
            "alertas_verdadeiros": round(res_campo["alertas_verdadeiros"], 3),
            "alertas_falsos": round(res_campo["alertas_falsos"], 3),
            "horas_gastas_falsos_alertas": round(res_campo["horas_alertas_falsos"], 2),
            "horas_gastas_totais": round(res_campo["horas_totais_inspecoes"], 2),
        },
        "item_d": {
            "sensibilidade_nova": sens_d,
            "taxa_falso_positivo": fpr,
            "vpp_novo": res_cenario_d["vpp"],
            "vpp_novo_percentual": round(res_cenario_d["vpp"] * 100, 2),
            "diferenca_vpp_pontos_percentuais": round((res_cenario_d["vpp"] - res_bayes["vpp"]) * 100, 2),
            "alertas_falsos_novo": round(res_campo_d["alertas_falsos"], 3),
            "horas_falsos_novo": round(res_campo_d["horas_alertas_falsos"], 2),
            "conclusao_tecnica": (
                "O aumento da sensibilidade de 95.0% para 99.9% eleva o VPP marginalmente de 60.96% "
                "para 62.15% (+1.19 p.p.), sem reduzir o numero de alarmes falsos (permanecem 22.87/semana "
                "e 4.57 horas desperdicadas). Por causa da baixa prevalencia (4.7%), a grande massa de talhoes "
                "sadios (95.3%) domina a geracao de falsos alertas pela Falacia da Taxa Base. "
                "Portanto, o gargalo operacional prioritario a ser atacado pela equipe de sensores e a "
                "REDUCAO DA TAXA DE FALSOS POSITIVOS (aumento da especificidade)."
            ),
        },
    }


def imprimir_relatorio_bayesiano(analise: Dict[str, Any]) -> None:
    """Exibe no terminal a dedução formal e os cálculos detalhados dos quatro itens."""
    params = analise["parametros"]
    ia = analise["item_a"]
    ib = analise["item_b"]
    ic = analise["item_c"]
    id_ = analise["item_d"]

    print("=" * 80)
    print("  Caatinga.AI - Analise Probabilistica Bayesiana do Sensor Optico de Pragas")
    print(f"  Semente Oficial: {analise['matricula']} (Secao 4.3 da Sprint 1)")
    print("=" * 80)

    print("\n[PARAMETROS OFICIAIS EXTRAIDOS DO GERADOR]")
    print(f"  - Prevalencia de Infestacao P(I):         {params['prevalencia'] * 100:.2f}% ({params['prevalencia']})")
    print(f"  - Sensibilidade do Sensor P(S+|I):        {params['sensibilidade'] * 100:.2f}% ({params['sensibilidade']})")
    print(f"  - Taxa de Falso Positivo P(S+|~I):        {params['taxa_falso_positivo'] * 100:.2f}% ({params['taxa_falso_positivo']})")
    print(f"  - Volume de Talhoes Inspecionados/semana: {params['talhoes_por_semana']}")

    print("\n" + "-" * 80)
    print("(a) Calculo Formal do Teorema de Bayes: P(Infestado | Sensor Positivo)")
    print("-" * 80)
    print("Definicao dos Eventos:")
    print("  - I : Talhao infestado por pragas  |  ~I : Talhao saudavel / nao infestado")
    print("  - S+: Sensor acusa positivo        |  S- : Sensor acusa negativo")
    print("\nFormula do Teorema de Bayes com Lei da Probabilidade Total:")
    print("                            P(S+ | I) * P(I)")
    print("  P(I | S+) = -------------------------------------------")
    print("              P(S+ | I) * P(I) + P(S+ | ~I) * P(~I)")
    print("\nSubstituicao passo a passo dos valores:")
    print(f"  - Numerador  = P(S+|I) * P(I) = {ia['sensibilidade']} * {ia['p_infestado']} = {ia['sensibilidade'] * ia['p_infestado']:.5f}")
    p_falsos_num = ia['taxa_falso_positivo'] * (1 - ia['p_infestado'])
    print(f"  - Parcela ~I = P(S+|~I) * P(~I) = {ia['taxa_falso_positivo']} * {1 - ia['p_infestado']:.3f} = {p_falsos_num:.5f}")
    print(f"  - Denominador P(S+) = {ia['sensibilidade'] * ia['p_infestado']:.5f} + {p_falsos_num:.5f} = {ia['p_sensor_positivo']:.5f}")
    print(f"  - P(I | S+) = {ia['sensibilidade'] * ia['p_infestado']:.5f} / {ia['p_sensor_positivo']:.5f} = {ia['vpp']:.6f} => {ia['vpp_percentual']}%\n")
    print(f"  => Resultado Final: O Valor Preditivo Positivo (VPP) e de {ia['vpp_percentual']}%.")

    print("\n" + "-" * 80)
    print("(b) Taxa de Alertas Falsos e Frase Complementada")
    print("-" * 80)
    print(f"  Taxa de Alertas Falsos (FDR = 1 - VPP): 1 - {ia['vpp']:.6f} = {ib['taxa_alertas_falsos']:.6f} ({ib['taxa_alertas_falsos_percentual']}%)")
    print("\n  Frase oficial completada conforme especificacao:")
    print(f"  >>> \"{ib['frase_completada']}\"")

    print("\n" + "-" * 80)
    print("(c) Impacto Operacional no Campo (800 talhoes/semana, 12 min/inspecao)")
    print("-" * 80)
    print(f"  - Total de talhoes examinados pelo sensor por semana: {ic['talhoes_por_semana']}")
    print(f"  - Total de alertas emitidos pelo sensor:             {ic['alertas_totais']:.2f}")
    print(f"    * Alertas verdadeiros (talhoes infestados):         {ic['alertas_verdadeiros']:.2f}")
    print(f"    * Alertas falsos (talhoes saudaveis):               {ic['alertas_falsos']:.2f}")
    print(f"  - Tempo por verificacao presencial em campo:         12 minutos (0.2 horas)")
    print(f"  - Horas semanais de agronomos em falsos alertas:     {ic['horas_gastas_falsos_alertas']:.2f} horas/semana (aprox. 4h 34min)")
    print(f"  - Horas semanais totais dedicadas a checagens:       {ic['horas_gastas_totais']:.2f} horas/semana")

    print("\n" + "-" * 80)
    print("(d) Cenario de Aumento de Sensibilidade (99.9%) vs Reducao de Falsos Positivos")
    print("-" * 80)
    print("Simulacao do Cenario:")
    print(f"  - Sensibilidade aumentada:  95.0% -> {id_['sensibilidade_nova'] * 100:.1f}%")
    print(f"  - Taxa de falso positivo:   mantida em {id_['taxa_falso_positivo'] * 100:.1f}%")
    print(f"  - Novo VPP:                 {id_['vpp_novo_percentual']}% (era {ia['vpp_percentual']}%)")
    print(f"  - Ganho efetivo no VPP:     +{id_['diferenca_vpp_pontos_percentuais']} pontos percentuais")
    print(f"  - Falsos alertas semanais:  {id_['alertas_falsos_novo']:.2f} (inalterado!)")
    print(f"  - Horas desperdicadas:      {id_['horas_falsos_novo']:.2f} horas/semana (inalterado!)")
    print("\nDiscussao Tecnica e Justificativa Agronomica:")
    print(f"  {id_['conclusao_tecnica']}")
    print("=" * 80)


if __name__ == "__main__":
    matricula = int(sys.argv[1]) if len(sys.argv) > 1 else 24114066
    analise = analisar_sensor_bayesiano(matricula)
    imprimir_relatorio_bayesiano(analise)
