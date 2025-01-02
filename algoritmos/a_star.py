from heapq import heappush, heappop

def a_star(graph, start, goal, heuristic):
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

        current_node = graph.get_node(current)  # Obter o nó atual como objeto Localidade
        if current_node:
            for neighbor in graph.get_neighbors(current_node):  # Explorar vizinhos
                route = graph.get_route(current_node, neighbor)  # Obter a rota
                if route and not route.bloqueado:  # Verificar se a rota não está bloqueada
                    tentative_g_cost = g_cost[current] + route.temp_cost
                    if neighbor.nome not in g_cost or tentative_g_cost < g_cost[neighbor.nome]:
                        g_cost[neighbor.nome] = tentative_g_cost
                        f_cost = tentative_g_cost + heuristic(neighbor, graph.get_node(goal))  # Passar objetos Localidade
                        heappush(open_set, (f_cost, neighbor.nome, path))

    return None, None  # Caminho não encontrado
