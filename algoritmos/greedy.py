from heapq import heappush, heappop

def greedy_search(graph, start, goal, heuristic, transport):
    """
    Implementa o algoritmo Greedy Search com cálculo de custo real acumulado.
    :param graph: Objeto do grafo.
    :param start: Nó inicial.
    :param goal: Nó objetivo.
    :param heuristic: Função heurística.
    :param transport: Objeto Transporte.
    :return: Tuplo (caminho, custo total) ou (None, None) se não for possível.
    """
    open_set = []  # Fila de prioridade para exploração
    visited = set()  # Conjunto de nós visitados

    # Adiciona o nó inicial à fila com custo acumulado 0
    start_node = graph.get_node(start)
    goal_node = graph.get_node(goal)
    heappush(open_set, (heuristic(start_node, goal_node), 0, start, []))  # (valor heurístico, custo acumulado, nó atual, caminho)

    while open_set:
        _, current_cost, current, path = heappop(open_set)
        path = path + [current]

        # Verifica se o objetivo foi alcançado
        if current == goal:
            return path, current_cost  # Caminho encontrado com custo acumulado

        if current in visited:
            continue

        visited.add(current)

        # Obter os vizinhos do nó atual
        current_node = graph.get_node(current)
        for neighbor in graph.get_neighbors(current_node):
            route = graph.get_route(current_node, neighbor)

            # Ignorar rotas inacessíveis
            if route and (route.bloqueado or not transport.can_access_route(route)):
                continue

            # Adiciona vizinhos acessíveis à fila de prioridade
            if neighbor.nome not in visited:
                heappush(
                    open_set,
                    (
                        heuristic(graph.get_node(neighbor.nome), goal_node),  # Valor heurístico
                        current_cost + route.temp_cost,  # Custo acumulado
                        neighbor.nome,  # Próximo nó
                        path,  # Caminho atual
                    ),
                )

    return None, None  # Caminho não encontrado
