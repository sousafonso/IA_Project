from heapq import heappush, heappop

def greedy_search(graph, start, goal, heuristic, transport):
    """

    Implementa o algoritmo Greedy Search com melhorias.
    :param graph: Objeto do grafo.
    :param start: Nó inicial.
    :param goal: Nó objetivo.
    :param heuristic: Função heurística.
    :param transport: Objeto Transporte.
    :return: Lista representando o caminho do início ao objetivo, ou None se não for possível.
    """
    open_set = []
    visited = set()
    heappush(open_set, (heuristic(start, goal, graph), start, []))  # (heurística, nó atual, caminho)


    while open_set:
        _, current, path = heappop(open_set)
        path = path + [current]

        if current == goal:
            return path  # Caminho encontrado

        if current in visited:
            continue

        visited.add(current)

        # Obter os vizinhos do nó atual
        current_node = graph.get_node(current)
        for neighbor in graph.get_neighbors(current_node):
            route = graph.get_route(current_node, neighbor)
            if route and route.bloqueado and not transport.can_access_route(route):
                continue  # Ignorar rotas inacessíveis

            if neighbor.nome not in visited:
                heappush(open_set, (heuristic(neighbor.nome, goal, graph), neighbor.nome, path))


    return None  # Caminho não encontrado


