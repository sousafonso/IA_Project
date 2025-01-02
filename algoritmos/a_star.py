from heapq import heappush, heappop

def a_star(graph, start, goal, heuristic):
    """
    Implementa o algoritmo A* com melhorias.
    :param graph: Dicionário {nó: [(vizinho, custo)]}.
    :param start: Nó inicial.
    :param goal: Nó objetivo.
    :param heuristic: Função heurística que estima o custo até o objetivo.
    :return: Lista representando o caminho do início ao objetivo, ou None se não for possível.
    """
    open_set = []
    heappush(open_set, (0, start, []))  # (custo estimado, nó atual, caminho)

    g_cost = {start: 0}  # Custo real do início até cada nó

    while open_set:
        _, current, path = heappop(open_set)
        path = path + [current]

        if current == goal:
            return path  # Caminho encontrado

        for neighbor, cost in graph.get(current, []):
            tentative_g_cost = g_cost[current] + cost
            if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g_cost
                f_cost = tentative_g_cost + heuristic(neighbor, goal)
                heappush(open_set, (f_cost, neighbor, path))

    return None  # Caminho não encontrado
