"""
Módulo de Algoritmos de Busca Cega e Informada para o Projeto Caatinga.AI.
Implementa:
  - BFS (Busca em Largura)
  - DFS (Busca em Profundidade)
  - UCS (Busca de Custo Uniforme)
  - A* (Busca A-Estrela com suporte a heurísticas e reabertura de nós)

Instrumenta os quatro contadores obrigatórios:
  1. Custo da rota
  2. Número de passos
  3. Quantidade de nós expandidos
  4. Tamanho máximo da fronteira
"""

import time
import heapq
from collections import deque
from typing import List, Tuple, Dict, Any, Callable, Optional
import os
import sys

# Garante que a raiz do repositório esteja no sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from src.gerador_pomar import CUSTO, BLOQUEADO, gerar_pomar
except ImportError:
    from gerador_pomar import CUSTO, BLOQUEADO, gerar_pomar

# Ordem fixa de expansão acordada pela dupla: De Sul a Norte
# 1. Sul: (+1, 0)
# 2. Leste: (0, +1)
# 3. Oeste: (0, -1)
# 4. Norte: (-1, 0)
DIRECOES: List[Tuple[int, int]] = [
    (1, 0),   # Sul
    (0, 1),   # Leste
    (0, -1),  # Oeste
    (-1, 0)   # Norte
]


def obter_vizinhos(r: int, c: int, pomar: List[List[str]], n: int) -> List[Tuple[int, int]]:
    """Retorna vizinhos ortogonais válidos na ordem estipulada: Sul, Leste, Oeste, Norte."""
    vizinhos = []
    for dr, dc in DIRECOES:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n and pomar[nr][nc] != BLOQUEADO:
            vizinhos.append((nr, nc))
    return vizinhos


def reconstruir_caminho(parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]],
                         goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Reconstrói o caminho a partir do dicionário de pais até o início."""
    curr = goal
    caminho = []
    while curr is not None:
        caminho.append(curr)
        curr = parent.get(curr)
    caminho.reverse()
    return caminho


def calcular_custo_caminho(caminho: List[Tuple[int, int]], pomar: List[List[str]]) -> int:
    """Calcula o custo total da rota (excluindo a célula de partida conforme especificação)."""
    if len(caminho) <= 1:
        return 0
    return sum(CUSTO[pomar[r][c]] for r, c in caminho[1:])


# --- Heurísticas para A* ---

def heuristica_zero(pos: Tuple[int, int], goal: Tuple[int, int]) -> int:
    """h1(n) = 0: heurística nula (reduz o A* ao UCS)."""
    return 0


def heuristica_manhattan(pos: Tuple[int, int], goal: Tuple[int, int]) -> int:
    """h2(n): Distância de Manhattan até o objetivo (admissível para custo mínimo >= 1)."""
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])


def heuristica_manhattan_4x(pos: Tuple[int, int], goal: Tuple[int, int]) -> int:
    """h3(n): 4 * Distância de Manhattan até o objetivo (inadmissível / inflacionada)."""
    return 4 * (abs(pos[0] - goal[0]) + abs(pos[1] - goal[1]))


# --- Algoritmos de Busca Cega ---

def busca_largura(pomar: List[List[str]],
                  inicio: Tuple[int, int] = (0, 0),
                  objetivo: Optional[Tuple[int, int]] = None) -> Dict[str, Any]:
    """
    Busca em Largura (BFS).
    Utiliza fila FIFO. Teste de objetivo realizado na geração dos nós sucessores.
    """
    n = len(pomar)
    if objetivo is None:
        objetivo = (n - 1, n - 1)

    t_inicio = time.perf_counter()

    if inicio == objetivo:
        t_fim = time.perf_counter()
        return {
            "estrategia": "BFS",
            "heuristica": "N/A",
            "caminho": [inicio],
            "custo": 0,
            "passos": 0,
            "nos_expandidos": 0,
            "fronteira_max": 1,
            "tempo_ms": (t_fim - t_inicio) * 1000.0,
            "otimo": True
        }

    queue = deque([inicio])
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {inicio: None}
    nos_expandidos = 0
    fronteira_max = 1
    encontrado = False

    while queue:
        fronteira_max = max(fronteira_max, len(queue))
        curr = queue.popleft()
        nos_expandidos += 1

        for viz in obter_vizinhos(curr[0], curr[1], pomar, n):
            if viz not in parent:
                parent[viz] = curr
                if viz == objetivo:
                    encontrado = True
                    break
                queue.append(viz)
        if encontrado:
            break

    t_fim = time.perf_counter()

    if not encontrado and objetivo not in parent:
        caminho = []
        custo = float("inf")
        passos = 0
    else:
        caminho = reconstruir_caminho(parent, objetivo)
        custo = calcular_custo_caminho(caminho, pomar)
        passos = len(caminho) - 1

    return {
        "estrategia": "BFS",
        "heuristica": "N/A",
        "caminho": caminho,
        "custo": custo,
        "passos": passos,
        "nos_expandidos": nos_expandidos,
        "fronteira_max": fronteira_max,
        "tempo_ms": (t_fim - t_inicio) * 1000.0,
        "otimo": False
    }


def busca_profundidade(pomar: List[List[str]],
                       inicio: Tuple[int, int] = (0, 0),
                       objetivo: Optional[Tuple[int, int]] = None) -> Dict[str, Any]:
    """
    Busca em Profundidade (DFS) em grafo.
    Utiliza pilha LIFO.
    Para manter a ordem de expansão Sul -> Leste -> Oeste -> Norte,
    os vizinhos são empilhados na ordem inversa (Norte, Oeste, Leste, Sul),
    garantindo que o topo da pilha retire primeiro o Sul.
    """
    n = len(pomar)
    if objetivo is None:
        objetivo = (n - 1, n - 1)

    t_inicio = time.perf_counter()

    stack = [inicio]
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {inicio: None}
    visitados = set()
    nos_expandidos = 0
    fronteira_max = 1
    encontrado = False

    while stack:
        fronteira_max = max(fronteira_max, len(stack))
        curr = stack.pop()

        if curr in visitados:
            continue
        visitados.add(curr)
        nos_expandidos += 1

        if curr == objetivo:
            encontrado = True
            break

        vizinhos = obter_vizinhos(curr[0], curr[1], pomar, n)
        # Empilha na ordem reversa para que o desempilhamento ocorra na ordem declarada:
        # Sul -> Leste -> Oeste -> Norte
        for viz in reversed(vizinhos):
            if viz not in visitados:
                parent[viz] = curr
                stack.append(viz)

    t_fim = time.perf_counter()

    if not encontrado:
        caminho = []
        custo = float("inf")
        passos = 0
    else:
        caminho = reconstruir_caminho(parent, objetivo)
        custo = calcular_custo_caminho(caminho, pomar)
        passos = len(caminho) - 1

    return {
        "estrategia": "DFS",
        "heuristica": "N/A",
        "caminho": caminho,
        "custo": custo,
        "passos": passos,
        "nos_expandidos": nos_expandidos,
        "fronteira_max": fronteira_max,
        "tempo_ms": (t_fim - t_inicio) * 1000.0,
        "otimo": False
    }


def busca_custo_uniforme(pomar: List[List[str]],
                         inicio: Tuple[int, int] = (0, 0),
                         objetivo: Optional[Tuple[int, int]] = None) -> Dict[str, Any]:
    """
    Busca de Custo Uniforme (UCS / Dijkstra).
    Utiliza fila de prioridade baseada no custo acumulado g(n).
    Teste de objetivo na expansão do nó. Suporta reabertura de caminhos mais baratos.
    """
    n = len(pomar)
    if objetivo is None:
        objetivo = (n - 1, n - 1)

    t_inicio = time.perf_counter()

    contador = 0
    pq = [(0, contador, inicio)]
    cost_so_far: Dict[Tuple[int, int], int] = {inicio: 0}
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {inicio: None}
    nos_expandidos = 0
    fronteira_max = 1
    encontrado = False

    while pq:
        fronteira_max = max(fronteira_max, len(pq))
        custo_atual, _, curr = heapq.heappop(pq)

        # Se o nó já foi alcançado por um custo estritamente menor, descarta
        if custo_atual > cost_so_far.get(curr, float("inf")):
            continue

        if curr == objetivo:
            encontrado = True
            break

        nos_expandidos += 1

        for viz in obter_vizinhos(curr[0], curr[1], pomar, n):
            custo_passo = CUSTO[pomar[viz[0]][viz[1]]]
            novo_custo = custo_atual + custo_passo

            # Reabertura/atualização de nó se encontrado caminho mais barato
            if viz not in cost_so_far or novo_custo < cost_so_far[viz]:
                cost_so_far[viz] = novo_custo
                parent[viz] = curr
                contador += 1
                heapq.heappush(pq, (novo_custo, contador, viz))

    t_fim = time.perf_counter()

    if not encontrado:
        caminho = []
        custo = float("inf")
        passos = 0
    else:
        caminho = reconstruir_caminho(parent, objetivo)
        custo = calcular_custo_caminho(caminho, pomar)
        passos = len(caminho) - 1

    return {
        "estrategia": "UCS",
        "heuristica": "N/A",
        "caminho": caminho,
        "custo": custo,
        "passos": passos,
        "nos_expandidos": nos_expandidos,
        "fronteira_max": fronteira_max,
        "tempo_ms": (t_fim - t_inicio) * 1000.0,
        "otimo": True
    }


# --- Algoritmo de Busca Informada: A* ---

def busca_a_estrela(pomar: List[List[str]],
                    heuristica: Callable[[Tuple[int, int], Tuple[int, int]], int] = heuristica_manhattan,
                    nome_heuristica: str = "Manhattan",
                    inicio: Tuple[int, int] = (0, 0),
                    objetivo: Optional[Tuple[int, int]] = None,
                    reabrir_nos: bool = True) -> Dict[str, Any]:
    """
    Algoritmo A* (A-Estrela).
    Utiliza fila de prioridade baseada em f(n) = g(n) + h(n).
    Teste de objetivo na expansão.
    Com reabrir_nos=True, atualiza a rota de nós mesmo que já visitados caso um caminho
    com menor g(n) seja descoberto (essencial para garantir otimalidade com heurísticas gerais).
    """
    n = len(pomar)
    if objetivo is None:
        objetivo = (n - 1, n - 1)

    t_inicio = time.perf_counter()

    contador = 0
    h_inicio = heuristica(inicio, objetivo)
    pq = [(h_inicio, 0, contador, inicio)]
    cost_so_far: Dict[Tuple[int, int], int] = {inicio: 0}
    parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {inicio: None}
    fechados = set()
    nos_expandidos = 0
    fronteira_max = 1
    encontrado = False

    while pq:
        fronteira_max = max(fronteira_max, len(pq))
        f_atual, g_atual, _, curr = heapq.heappop(pq)

        # Se não reabrimos nós fechados e o nó já foi expandido
        if not reabrir_nos and curr in fechados:
            continue

        # Se já encontramos um custo g melhor que este registro da fila, descarta
        if g_atual > cost_so_far.get(curr, float("inf")):
            continue

        if curr == objetivo:
            encontrado = True
            break

        fechados.add(curr)
        nos_expandidos += 1

        for viz in obter_vizinhos(curr[0], curr[1], pomar, n):
            custo_passo = CUSTO[pomar[viz[0]][viz[1]]]
            novo_g = g_atual + custo_passo

            # Se nó já fechado e reabertura está desativada, ignora
            if not reabrir_nos and viz in fechados:
                continue

            if viz not in cost_so_far or novo_g < cost_so_far[viz]:
                cost_so_far[viz] = novo_g
                parent[viz] = curr
                contador += 1
                novo_h = heuristica(viz, objetivo)
                novo_f = novo_g + novo_h
                heapq.heappush(pq, (novo_f, novo_g, contador, viz))

    t_fim = time.perf_counter()

    if not encontrado:
        caminho = []
        custo = float("inf")
        passos = 0
    else:
        caminho = reconstruir_caminho(parent, objetivo)
        custo = calcular_custo_caminho(caminho, pomar)
        passos = len(caminho) - 1

    return {
        "estrategia": "A*",
        "heuristica": nome_heuristica,
        "caminho": caminho,
        "custo": custo,
        "passos": passos,
        "nos_expandidos": nos_expandidos,
        "fronteira_max": fronteira_max,
        "tempo_ms": (t_fim - t_inicio) * 1000.0,
        "otimo": (nome_heuristica in ["h1 (zero)", "h2 (Manhattan)", "Manhattan", "zero"])
    }


def executar_todas_as_buscas(matricula: int) -> List[Dict[str, Any]]:
    """Executa todos os métodos sobre o pomar gerado pela matrícula fornecida."""
    pomar = gerar_pomar(matricula)
    
    resultados = [
        busca_largura(pomar),
        busca_profundidade(pomar),
        busca_custo_uniforme(pomar),
        busca_a_estrela(pomar, heuristica_zero, "h1 (zero)"),
        busca_a_estrela(pomar, heuristica_manhattan, "h2 (Manhattan)"),
        busca_a_estrela(pomar, heuristica_manhattan_4x, "h3 (4x Manhattan)"),
    ]
    return resultados


if __name__ == "__main__":
    import sys
    matricula = int(sys.argv[1]) if len(sys.argv) > 1 else 24114066
    print(f"=== Executando buscas para a matrícula: {matricula} ===")
    res = executar_todas_as_buscas(matricula)
    print(f"{'Estratégia':<10} | {'Heurística':<18} | {'Custo':<6} | {'Passos':<7} | {'Expandidos':<10} | {'Fronteira Máx':<13} | {'Tempo (ms)':<10}")
    print("-" * 88)
    for r in res:
        print(f"{r['estrategia']:<10} | {r['heuristica']:<18} | {r['custo']:<6} | {r['passos']:<7} | {r['nos_expandidos']:<10} | {r['fronteira_max']:<13} | {r['tempo_ms']:<10.3f}")
