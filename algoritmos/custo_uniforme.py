from heapq import heappush, heappop

def uniform_cost_search(graph, start, goal, transport):
    """
    Implementa o algoritmo de Custo Uniforme.
    :param graph: Objeto Grafo.
    :param start: Nó inicial.
    :param goal: Nó objetivo.
    :param transport: Objeto Transporte.
    :return: Lista representando o caminho, ou None se não for possível.
    """
    priority_queue = []  # (custo acumulado, nó atual, caminho)
    heappush(priority_queue, (0, start, []))
    visited = set()

    while priority_queue:
        cost, current, path = heappop(priority_queue)
        path = path + [current]

        if current == goal:
            return path  # Caminho encontrado

        if current not in visited:
            visited.add(current)

            current_node = graph.get_node(current)
            for neighbor in graph.get_neighbors(current_node):
                route = graph.get_route(current_node, neighbor)
                if route.bloqueado and not transport.can_access_route(route):
                    continue  # Ignorar rotas inacessíveis

                heappush(priority_queue, (cost + route.distancia, neighbor.nome, path))

    return None  # Caminho não encontrado

