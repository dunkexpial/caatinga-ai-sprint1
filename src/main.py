"""
Script Principal Unificado do Projeto Caatinga.AI.
Disciplina: Inteligência Artificial - Prof. Ronierison Maciel - UniRios 2026.2
Dupla: João Vítor Almeida dos Santos & Caio Lúcio dos Santos Almeida
Semente Oficial: 24114066

Atende ao Requisito 4 da Seção 9.1:
  "Um comando para rodar tudo: python src/main.py <matricula> deve gerar
   resultados.csv, grafico.png e pomar.txt do zero."
"""

import csv
import os
import sys
import time
from typing import Any, Dict, List

# Configuração do Matplotlib para execução sem display gráfico interativo
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Garante que a raiz do repositório esteja no sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from src.gerador_pomar import BLOQUEADO, CUSTO, gerar_pomar, parametros_sensor
    from src.buscas import (
        heuristica_zero,
        heuristica_manhattan,
        heuristica_manhattan_4x,
        busca_largura,
        busca_profundidade,
        busca_custo_uniforme,
        busca_a_estrela,
        executar_todas_as_buscas,
    )
    from src.busca_local import executar_experimento_busca_local
    from src.especialista import executar_caso_estudo_quebra_base
    from src.bayes import analisar_sensor_bayesiano
except ImportError:
    from gerador_pomar import BLOQUEADO, CUSTO, gerar_pomar, parametros_sensor
    from buscas import (
        heuristica_zero,
        heuristica_manhattan,
        heuristica_manhattan_4x,
        busca_largura,
        busca_profundidade,
        busca_custo_uniforme,
        busca_a_estrela,
        executar_todas_as_buscas,
    )
    from busca_local import executar_experimento_busca_local
    from especialista import executar_caso_estudo_quebra_base
    from bayes import analisar_sensor_bayesiano


def salvar_pomar_txt(pomar: List[List[str]], matricula: int, caminho_txt: str) -> None:
    """
    Gera o arquivo pomar.txt conforme especificação da Seção 9.1:
      'pomar.txt <- sua grade; matrícula-semente na 1ª linha'
    """
    os.makedirs(os.path.dirname(caminho_txt), exist_ok=True)
    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write(f"{matricula}\n")
        for linha in pomar:
            f.write(" ".join(linha) + "\n")


def salvar_resultados_csv(resultados: List[Dict[str, Any]], caminho_csv: str) -> None:
    """
    Gera o arquivo resultados.csv com os cabeçalhos obrigatórios da Seção 9.1:
      estrategia,heuristica,custo,passos,nos_expandidos,fronteira_max,tempo_ms
    """
    os.makedirs(os.path.dirname(caminho_csv), exist_ok=True)
    cabecalhos = [
        "estrategia",
        "heuristica",
        "custo",
        "passos",
        "nos_expandidos",
        "fronteira_max",
        "tempo_ms",
    ]
    with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(cabecalhos)
        for r in resultados:
            writer.writerow([
                r["estrategia"],
                r["heuristica"],
                r["custo"],
                r["passos"],
                r["nos_expandidos"],
                r["fronteira_max"],
                f"{r['tempo_ms']:.3f}",
            ])


def gerar_grafico_nos_expandidos(resultados: List[Dict[str, Any]], matricula: int, caminho_png: str) -> None:
    """
    Gera e salva o gráfico comparativo de nós expandidos por estratégia.
    Atende à Seção 9.1 e à Regra 11 de avaliação ('com eixos rotulados e unidade').
    """
    os.makedirs(os.path.dirname(caminho_png), exist_ok=True)

    rotulos = []
    valores = []
    cores = []

    # Paleta profissional diferenciada para buscas cegas e informadas
    paleta = {
        "BFS": "#3498db",               # Azul
        "DFS": "#e67e22",               # Laranja
        "UCS": "#2ecc71",               # Verde esmeralda (ótimo cego)
        "h1 (zero)": "#95a5a6",         # Cinza
        "h2 (Manhattan)": "#27ae60",    # Verde escuro (A* ótimo informado)
        "h3 (4x Manhattan)": "#e74c3c"  # Vermelho (A* inflacionado/subótimo)
    }

    for r in resultados:
        if r["heuristica"] == "N/A":
            nome = r["estrategia"]
            cor = paleta.get(nome, "#34495e")
        else:
            nome = f"{r['estrategia']}\n{r['heuristica']}"
            cor = paleta.get(r["heuristica"], "#9b59b6")
        rotulos.append(nome)
        valores.append(r["nos_expandidos"])
        cores.append(cor)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    barras = ax.bar(rotulos, valores, color=cores, width=0.55, edgecolor="#2c3e50", linewidth=1.2, zorder=3)

    # Rótulo de dados sobre cada barra
    ax.bar_label(barras, padding=4, fontsize=11, fontweight="bold", color="#2c3e50")

    # Títulos e Eixos rotulados obrigatoriamente com unidade
    ax.set_title(
        f"Nós Expandidos por Estratégia de Busca no Pomar 12x12\n(Semente Oficial: {matricula} | UniRios 2026.2)",
        fontsize=13,
        fontweight="bold",
        pad=15
    )
    ax.set_xlabel("Estratégia de Busca / Heurística", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_ylabel("Nós Expandidos (quantidade de estados)", fontsize=11, fontweight="bold", labelpad=10)

    # Grade horizontal de suporte
    ax.yaxis.grid(True, linestyle="--", alpha=0.5, zorder=0)
    ax.set_axisbelow(True)

    # Margem superior para acomodar rótulos
    lim_y = max(valores) * 1.15 if valores else 100
    ax.set_ylim(0, lim_y)

    # Nota de rodapé explicativa
    plt.figtext(
        0.5,
        -0.03,
        "Ordem de expansão declarada: Sul -> Leste -> Oeste -> Norte. "
        "A* com reabertura de nós ativada.",
        ha="center",
        fontsize=9,
        style="italic",
        color="#555555"
    )

    plt.tight_layout()
    plt.savefig(caminho_png, dpi=300, bbox_inches="tight")
    plt.close()


def executar_pipeline_completo(matricula: int = 24114066) -> None:
    """Executa o pipeline completo do Caatinga.AI, gerando todos os artefatos da pasta resultados/."""
    diretorio_resultados = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resultados"))
    caminho_pomar = os.path.join(diretorio_resultados, "pomar.txt")
    caminho_csv = os.path.join(diretorio_resultados, "resultados.csv")
    caminho_grafico = os.path.join(diretorio_resultados, "grafico.png")

    print("=" * 86)
    print("  CAATINGA.AI - SISTEMA INTEGRADO DE NAVEGAÇÃO E INSPEÇÃO FITOSSANITÁRIA")
    print(f"  Dupla: João Vítor Almeida dos Santos & Caio Lúcio dos Santos Almeida")
    print(f"  Semente Oficial de Execução: {matricula} (Matrícula do integrante mais velho)")
    print("=" * 86)

    # 1. Geração do Pomar 12x12
    print("\n[1/5] Gerando pomar 12x12 e salvando em resultados/pomar.txt...")
    pomar = gerar_pomar(matricula)
    salvar_pomar_txt(pomar, matricula, caminho_pomar)
    print(f"  [OK] Pomar salvo com sucesso em: {caminho_pomar}")

    # Exibe a grade no console
    print("\nGrade do Pomar (S = Portão (0,0), G = Coleta (11,11)):")
    for r, linha in enumerate(pomar):
        print(f"  {r:2d} | " + " ".join(linha))

    # Contagem de células
    n_carreador = sum(row.count(".") for row in pomar)
    n_encharcado = sum(row.count("~") for row in pomar)
    n_bloqueado = sum(row.count("#") for row in pomar)
    print(f"\n  Resumo do terreno: {n_carreador} carreadores (.), {n_encharcado} encharcados (~), {n_bloqueado} bloqueados (#)")

    # 2. Execução das Buscas (BFS, DFS, UCS, A* h1, A* h2, A* h3)
    print("\n" + "-" * 86)
    print("[2/5] Executando algoritmos de busca clássica e informada (A*)...")
    resultados_buscas = executar_todas_as_buscas(matricula)

    # Exibição tabular no terminal
    print(f"\n{'Estratégia':<10} | {'Heurística':<18} | {'Custo':<6} | {'Passos':<7} | {'Expandidos':<10} | {'Fronteira Máx':<13} | {'Tempo (ms)':<10}")
    print("-" * 86)
    for r in resultados_buscas:
        print(f"{r['estrategia']:<10} | {r['heuristica']:<18} | {r['custo']:<6} | {r['passos']:<7} | {r['nos_expandidos']:<10} | {r['fronteira_max']:<13} | {r['tempo_ms']:<10.3f}")

    # 3. Exportação do CSV e Geração do Gráfico
    print("\n" + "-" * 86)
    print("[3/5] Gerando resultados.csv e grafico.png...")
    salvar_resultados_csv(resultados_buscas, caminho_csv)
    print(f"  [OK] CSV salvo com sucesso em: {caminho_csv}")

    gerar_grafico_nos_expandidos(resultados_buscas, matricula, caminho_grafico)
    print(f"  [OK] Gráfico salvo com sucesso em: {caminho_grafico}")

    # 4. Síntese da Busca Local (K=15)
    print("\n" + "-" * 86)
    print("[4/5] Executando protocolo experimental de busca local (K=15, 30 execuções)...")
    dados_local = executar_experimento_busca_local(matricula=matricula, k=15, num_execucoes=30)
    hc = dados_local["hill_climbing"]
    sa = dados_local["simulated_annealing"]
    print(f"  - Hill Climbing:       Média = {hc['media']:.2f} | Desvio = {hc['desvio_padrao']:.2f} | Melhor = {hc['melhor_valor']:.2f} | Tempo = {hc['tempo_medio_ms']:.1f} ms")
    print(f"  - Simulated Annealing: Média = {sa['media']:.2f} | Desvio = {sa['desvio_padrao']:.2f} | Melhor = {sa['melhor_valor']:.2f} | Tempo = {sa['tempo_medio_ms']:.1f} ms")

    # 5. Síntese do Sistema Especialista e Modelo Bayesiano
    print("\n" + "-" * 86)
    print("[5/5] Executando Sistema Especialista (Backward Chaining) e Análise Bayesiana...")
    caso_esp = executar_caso_estudo_quebra_base()
    print(f"  - Sistema Especialista: Base v1 permitia pulverização química ilegal ({caso_esp['v1_quimico_provado']}).")
    print(f"                          Base v2 com salvaguarda R7 acionou controle biológico ({caso_esp['v2_biologico_provado']}).")

    res_bayes = analisar_sensor_bayesiano(matricula)
    vpp = res_bayes["item_a"]["vpp_percentual"]
    falsos_100 = round(res_bayes["item_b"]["taxa_alertas_falsos"] * 100)
    horas_falsas = res_bayes["item_c"]["horas_gastas_falsos_alertas"]
    print(f"  - Modelo Bayesiano:     VPP = {vpp}% | Alertas Falsos: {falsos_100} a cada 100 alertas.")
    print(f"                          Horas de agrônomos gastas com falsos alertas: {horas_falsas:.2f} h/semana.")

    print("\n" + "=" * 86)
    print("  PIPELINE EXECUTADO COM SUCESSO!")
    print("  Todos os arquivos requeridos foram gerados na pasta 'resultados/':")
    print(f"    * {caminho_pomar}")
    print(f"    * {caminho_csv}")
    print(f"    * {caminho_grafico}")
    print("=" * 86 + "\n")


if __name__ == "__main__":
    matricula_cmd = int(sys.argv[1]) if len(sys.argv) > 1 else 24114066
    executar_pipeline_completo(matricula_cmd)
