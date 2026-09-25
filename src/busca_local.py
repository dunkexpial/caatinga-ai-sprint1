"""
Módulo de Busca Local para Inspeção de Talhões no Projeto Caatinga.AI.
Atende à Seção 5.4 do enunciado e requisitos da Sprint 1.

Implementa:
  - Subida de Encosta (Hill Climbing - Steepest Ascent / Ganancioso tradicional)
  - Têmpera Simulada (Simulated Annealing com resfriamento geométrico)

Problema:
  - Selecionar K = 15 talhões livres para inspeção fitossanitária no pomar 12x12.
  - Modelagem da vizinhança: 1-opt swap (trocar 1 talhão inspecionado por 1 livre não inspecionado).
  - Função Objetivo: Maximizar o escore combinado de severidade agronômica de pragas/umidade
    e dispersão espacial (cobertura homogênea pela grade).
  - Execução experimental: 30 rodadas independentes para análise estatística
    (Média, Desvio Padrão e Melhor Valor).
"""

import math
import os
import random
import statistics
import sys
import time
from typing import Any, Dict, List, Optional, Set, Tuple

# Garante que a raiz do repositório esteja no sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from src.gerador_pomar import BLOQUEADO, gerar_pomar
except ImportError:
    from gerador_pomar import BLOQUEADO, gerar_pomar


def dist_manhattan(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calcula a distância de Manhattan entre duas coordenadas (r, c)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def obter_talhoes_livres(pomar: List[List[str]]) -> List[Tuple[int, int]]:
    """
    Retorna a lista de todas as coordenadas livres (r, c) do pomar,
    isto é, células transitáveis que não são bloqueadas ('#').
    """
    n = len(pomar)
    return [
        (r, c)
        for r in range(n)
        for c in range(n)
        if pomar[r][c] != BLOQUEADO
    ]


def calcular_mapa_risco(pomar: List[List[str]],
                         livres: List[Tuple[int, int]]) -> Dict[Tuple[int, int], float]:
    """
    Pré-calcula a pontuação de severidade de pragas/risco fitossanitário para cada talhão livre.
    
    Critérios:
      - Solo encharcado ('~'): foco crítico de umidade e proliferação de pragas/fungos (peso base 10.0).
      - Carreador ('.'): tráfego regular, risco basal (peso base 2.0).
      - Proximidade com focos de umidade: soma da influência inversa da distância
        até os focos de solo encharcado do pomar.
    """
    n = len(pomar)
    focos_umidade = [
        (r, c)
        for r in range(n)
        for c in range(n)
        if pomar[r][c] == "~"
    ]

    mapa_risco: Dict[Tuple[int, int], float] = {}
    for p in livres:
        base = 10.0 if pomar[p[0]][p[1]] == "~" else 2.0
        # Influência cumulativa de zonas úmidas vizinhas
        influencia_umidade = sum(
            3.0 / (1.0 + dist_manhattan(p, w))
            for w in focos_umidade
        )
        mapa_risco[p] = round(base + influencia_umidade, 4)

    return mapa_risco


def precomputar_estrutura(pomar: List[List[str]], livres: List[Tuple[int, int]]):
    """
    Pré-computa matriz de distâncias e array de riscos indexados por inteiros
    para otimizar as avaliações de vizinhança nas buscas locais.
    """
    n_livres = len(livres)
    mapa_risco = calcular_mapa_risco(pomar, livres)
    risco_array = [mapa_risco[livres[i]] for i in range(n_livres)]
    dist_matriz = [
        [dist_manhattan(livres[i], livres[j]) for j in range(n_livres)]
        for i in range(n_livres)
    ]
    return mapa_risco, risco_array, dist_matriz


def calcular_funcao_objetivo_indices(indices: Set[int],
                                     risco_array: List[float],
                                     dist_matriz: List[List[int]],
                                     lambda_dispersao: float = 2.0) -> float:
    """
    Função objetivo avaliada sobre índices inteiros dos talhões.
    Combina risco agronômico fitossanitário e dispersão espacial mínima.
    """
    if not indices:
        return 0.0

    score_risco = sum(risco_array[i] for i in indices)
    score_disp = 0
    for i in indices:
        score_disp += min(dist_matriz[i][j] for j in indices if j != i)

    return round(score_risco + lambda_dispersao * score_disp, 4)


def funcao_objetivo(estado: Set[Tuple[int, int]],
                    mapa_risco: Dict[Tuple[int, int], float],
                    lambda_dispersao: float = 2.0) -> float:
    """
    Interface pública da função objetivo sobre conjunto de coordenadas (r, c).
    """
    if not estado:
        return 0.0

    score_risco = sum(mapa_risco[p] for p in estado)
    score_disp = 0
    for p in estado:
        score_disp += min(dist_manhattan(p, q) for q in estado if q != p)

    return round(score_risco + lambda_dispersao * score_disp, 4)


def hill_climbing(livres: List[Tuple[int, int]],
                  mapa_risco: Dict[Tuple[int, int], float],
                  k: int = 15,
                  rng: Optional[random.Random] = None,
                  max_iter: int = 100,
                  lambda_dispersao: float = 2.0,
                  dist_matriz: Optional[List[List[int]]] = None,
                  risco_array: Optional[List[float]] = None) -> Dict[str, Any]:
    """
    Algoritmo de Subida de Encosta (Hill Climbing - Steepest Ascent).
    
    Operador de Vizinhança: 1-opt swap.
    A cada iteração, avalia toda a vizinhança 1-opt e seleciona a troca que gera
    o maior ganho estrito. Encerra ao atingir um ótimo local (sem melhoria possível).
    """
    if rng is None:
        rng = random.Random()

    t_inicio = time.perf_counter()
    n_livres = len(livres)

    if dist_matriz is None or risco_array is None:
        risco_array = [mapa_risco[livres[i]] for i in range(n_livres)]
        dist_matriz = [
            [dist_manhattan(livres[i], livres[j]) for j in range(n_livres)]
            for i in range(n_livres)
        ]

    todos_indices = list(range(n_livres))
    atual = set(rng.sample(todos_indices, k))
    val_atual = calcular_funcao_objetivo_indices(atual, risco_array, dist_matriz, lambda_dispersao)

    avaliacoes = 1
    iteracoes = 0

    for it in range(max_iter):
        iteracoes += 1
        melhor_vizinho = None
        melhor_val = val_atual
        candidatos_fora = [x for x in todos_indices if x not in atual]

        for u in list(atual):
            for v in candidatos_fora:
                vizinho = (atual - {u}) | {v}
                avaliacoes += 1
                val_vizinho = calcular_funcao_objetivo_indices(vizinho, risco_array, dist_matriz, lambda_dispersao)
                if val_vizinho > melhor_val:
                    melhor_val = val_vizinho
                    melhor_vizinho = vizinho

        if melhor_vizinho is None or melhor_val <= val_atual + 1e-9:
            break

        atual = melhor_vizinho
        val_atual = melhor_val

    t_fim = time.perf_counter()

    melhor_coords = sorted([livres[i] for i in atual])

    return {
        "algoritmo": "Hill Climbing",
        "melhor_valor": val_atual,
        "melhor_estado": melhor_coords,
        "iteracoes": iteracoes,
        "avaliacoes": avaliacoes,
        "tempo_ms": (t_fim - t_inicio) * 1000.0,
    }


def simulated_annealing(livres: List[Tuple[int, int]],
                        mapa_risco: Dict[Tuple[int, int], float],
                        k: int = 15,
                        rng: Optional[random.Random] = None,
                        t0: float = 100.0,
                        alpha: float = 0.995,
                        t_min: float = 1e-4,
                        max_iter: int = 3000,
                        lambda_dispersao: float = 2.0,
                        dist_matriz: Optional[List[List[int]]] = None,
                        risco_array: Optional[List[float]] = None) -> Dict[str, Any]:
    """
    Algoritmo de Têmpera Simulada (Simulated Annealing).
    
    Operador de Vizinhança: 1-opt swap estocástico.
    A cada passo, seleciona um vizinho aleatório. Se a mudança melhorar a função
    objetivo (delta > 0), a transição é aceita. Se piorar (delta <= 0), a transição
    é aceita com probabilidade P = exp(delta / T).
    
    Programação de Resfriamento: T(t) = T0 * (alpha ^ t).
    Rastreia e preserva a melhor solução global encontrada ao longo da trajetória.
    """
    if rng is None:
        rng = random.Random()

    t_inicio = time.perf_counter()
    n_livres = len(livres)

    if dist_matriz is None or risco_array is None:
        risco_array = [mapa_risco[livres[i]] for i in range(n_livres)]
        dist_matriz = [
            [dist_manhattan(livres[i], livres[j]) for j in range(n_livres)]
            for i in range(n_livres)
        ]

    todos_indices = list(range(n_livres))
    atual = set(rng.sample(todos_indices, k))
    val_atual = calcular_funcao_objetivo_indices(atual, risco_array, dist_matriz, lambda_dispersao)

    melhor_indices = set(atual)
    melhor_val = val_atual

    t = t0
    iteracoes = 0
    pioras_aceitas = 0

    for it in range(max_iter):
        iteracoes += 1
        candidatos_fora = [x for x in todos_indices if x not in atual]
        u = rng.choice(list(atual))
        v = rng.choice(candidatos_fora)

        vizinho = (atual - {u}) | {v}
        val_vizinho = calcular_funcao_objetivo_indices(vizinho, risco_array, dist_matriz, lambda_dispersao)

        delta = val_vizinho - val_atual

        if delta > 0:
            atual = vizinho
            val_atual = val_vizinho
            if val_atual > melhor_val:
                melhor_val = val_atual
                melhor_indices = set(atual)
        else:
            prob = math.exp(delta / max(t, 1e-9))
            if rng.random() < prob:
                atual = vizinho
                val_atual = val_vizinho
                pioras_aceitas += 1

        t *= alpha
        if t < t_min:
            break

    t_fim = time.perf_counter()

    melhor_coords = sorted([livres[i] for i in melhor_indices])

    return {
        "algoritmo": "Simulated Annealing",
        "melhor_valor": melhor_val,
        "melhor_estado": melhor_coords,
        "iteracoes": iteracoes,
        "pioras_aceitas": pioras_aceitas,
        "temperatura_final": t,
        "tempo_ms": (t_fim - t_inicio) * 1000.0,
    }


def executar_experimento_busca_local(matricula: int = 24114066,
                                     k: int = 15,
                                     num_execucoes: int = 30) -> Dict[str, Any]:
    """
    Executa o protocolo experimental completo de 30 rodadas independentes para
    Hill Climbing e Simulated Annealing sobre o pomar gerado pela matrícula fornecida.
    
    Reporta: Média, Desvio Padrão e Melhor Valor (Score Máximo).
    """
    pomar = gerar_pomar(matricula)
    livres = obter_talhoes_livres(pomar)
    mapa_risco, risco_array, dist_matriz = precomputar_estrutura(pomar, livres)

    resultados_hc: List[Dict[str, Any]] = []
    resultados_sa: List[Dict[str, Any]] = []

    for i in range(num_execucoes):
        rng_hc = random.Random(100_000 + i)
        rng_sa = random.Random(200_000 + i)

        res_hc = hill_climbing(livres, mapa_risco, k=k, rng=rng_hc,
                               dist_matriz=dist_matriz, risco_array=risco_array)
        res_sa = simulated_annealing(livres, mapa_risco, k=k, rng=rng_sa,
                                     dist_matriz=dist_matriz, risco_array=risco_array)

        resultados_hc.append(res_hc)
        resultados_sa.append(res_sa)

    valores_hc = [r["melhor_valor"] for r in resultados_hc]
    valores_sa = [r["melhor_valor"] for r in resultados_sa]
    tempos_hc = [r["tempo_ms"] for r in resultados_hc]
    tempos_sa = [r["tempo_ms"] for r in resultados_sa]

    melhor_hc = max(resultados_hc, key=lambda x: x["melhor_valor"])
    melhor_sa = max(resultados_sa, key=lambda x: x["melhor_valor"])

    estatisticas = {
        "matricula": matricula,
        "k": k,
        "num_execucoes": num_execucoes,
        "total_livres": len(livres),
        "hill_climbing": {
            "media": round(statistics.mean(valores_hc), 2),
            "desvio_padrao": round(statistics.stdev(valores_hc), 2) if len(valores_hc) > 1 else 0.0,
            "melhor_valor": round(max(valores_hc), 2),
            "pior_valor": round(min(valores_hc), 2),
            "tempo_medio_ms": round(statistics.mean(tempos_hc), 2),
            "melhor_solucao": melhor_hc["melhor_estado"],
        },
        "simulated_annealing": {
            "media": round(statistics.mean(valores_sa), 2),
            "desvio_padrao": round(statistics.stdev(valores_sa), 2) if len(valores_sa) > 1 else 0.0,
            "melhor_valor": round(max(valores_sa), 2),
            "pior_valor": round(min(valores_sa), 2),
            "tempo_medio_ms": round(statistics.mean(tempos_sa), 2),
            "melhor_solucao": melhor_sa["melhor_estado"],
        },
    }

    return estatisticas


if __name__ == "__main__":
    matricula = int(sys.argv[1]) if len(sys.argv) > 1 else 24114066
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 15

    print("=" * 76)
    print(f"  Caatinga.AI - Otimização de Inspeção por Busca Local (K={k})")
    print(f"  Semente Oficial: {matricula} | 30 Execuções Independentes")
    print("=" * 76 + "\n")

    dados = executar_experimento_busca_local(matricula=matricula, k=k, num_execucoes=30)
    hc = dados["hill_climbing"]
    sa = dados["simulated_annealing"]

    print(f"Talhões livres disponíveis: {dados['total_livres']} de 144")
    print(f"Espaço combinatório C({dados['total_livres']}, {k}) ~ 2.45 x 10^18 combinações\n")

    print(f"{'Algoritmo':<22} | {'Média':<8} | {'Desvio Padrão':<14} | {'Melhor Valor':<13} | {'Tempo Médio':<12}")
    print("-" * 76)
    print(f"{'Hill Climbing':<22} | {hc['media']:<8.2f} | {hc['desvio_padrao']:<14.2f} | {hc['melhor_valor']:<13.2f} | {hc['tempo_medio_ms']:<7.1f} ms")
    print(f"{'Simulated Annealing':<22} | {sa['media']:<8.2f} | {sa['desvio_padrao']:<14.2f} | {sa['melhor_valor']:<13.2f} | {sa['tempo_medio_ms']:<7.1f} ms")
    print("-" * 76)

    print(f"\nMelhor subconjunto de talhões (Hill Climbing):")
    print(f"  {hc['melhor_solucao']}")
    print(f"\nMelhor subconjunto de talhões (Simulated Annealing):")
    print(f"  {sa['melhor_solucao']}")
    print("\n[OK] Experimento concluído com sucesso.")
