from heapq import heappush, heappop

def a_star(graph, start, goal, heuristic,transport):
    """
    Implementa o algoritmo A* com base no custo temporário (tempo de viagem).
    :param graph: Objeto da classe Grafo.
    :param start: Identificador do nó inicial (string).
    :param goal: Identificador do nó objetivo (string).
    :param heuristic: Função heurística que estima o custo até o objetivo.
    :return: Tuplo (caminho, custo total) ou (None, None) se não for possível.
    """
    open_set = []
    heappush(open_set, (0, start, []))  # (custo estimado, nó atual, caminho)

    g_cost = {start: 0}  # Custo real do início até cada nó

    while open_set:
        _, current, path = heappop(open_set)
        path = path + [current]

        if current == goal:
            return path, g_cost[current]  # Caminho e custo encontrados

        for neighbor, cost in graph.get(current, []):
            # Verificar se a rota está bloqueada
            route = graph.get_route(current, neighbor)
            if route.bloqueado and not transport.can_access_route(route):  # Ignorar rotas bloqueadas
                continue
            tentative_g_cost = g_cost[current] + route.temp_cost
            if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g_cost
                f_cost = tentative_g_cost + heuristic(neighbor, goal)
                heappush(open_set, (f_cost, neighbor, path))


    return None, None  # Caminho não encontrado
