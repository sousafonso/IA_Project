from heapq import heappush, heappop

def greedy_search(graph, start, goal, heuristic):
    """
    Implementa o algoritmo Greedy Search com melhorias.
    :param graph: Dicionário {nó: [(vizinho, custo)]}.
    :param start: Nó inicial.
    :param goal: Nó objetivo.
    :param heuristic: Função heurística que estima o custo até o objetivo.
    :return: Lista representando o caminho do início ao objetivo, ou None se não for possível.
    """
    open_set = []
    visited = set()
    heappush(open_set, (heuristic(start, goal), start, []))  # (heurística, nó atual, caminho)

    while open_set:
        _, current, path = heappop(open_set)
        path = path + [current]

        if current == goal:
            return path  # Caminho encontrado

        if current in visited:
            continue

        visited.add(current)

        for neighbor, cost in graph.get(current, []):
            if neighbor not in visited:
                heappush(open_set, (heuristic(neighbor, goal), neighbor, path))

    return None  # Caminho não encontrado
