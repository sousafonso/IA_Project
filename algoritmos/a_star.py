from heapq import heappush, heappop

def a_star(graph, start, goal, heuristic, transport):
    """
    Implementa o algoritmo A* com base no custo temporário (tempo de viagem).
    Caso uma rota esteja bloqueada, tenta encontrar caminhos alternativos.
    :param graph: Objeto da classe Grafo.
    :param start: Identificador do nó inicial (string).
    :param goal: Identificador do nó objetivo (string).
    :param heuristic: Função heurística que estima o custo até o objetivo.
    :param transport: Objeto Transporte, que define o tipo de transporte usado.
    :return: Tuplo (caminho, custo total) ou (None, None) se não for possível.
    """
    open_set = []  # Fila de prioridade para exploração
    heappush(open_set, (0, start, []))  # (custo estimado, nó atual, caminho)
    
    g_cost = {start: 0}  # Custo real do início até cada nó
    fallback_routes = []  # Lista para rotas bloqueadas

    while open_set:
        _, current, path = heappop(open_set)
        path = path + [current]

        # Verifica se o objetivo foi alcançado
        if current == goal:
            return path, g_cost[current]

        # Explora os vizinhos do nó atual
        current_node = graph.get_node(current)
        if current_node:
            for neighbor in graph.get_neighbors(current_node):  # Obter vizinhos
                route = graph.get_route(current_node, neighbor)

                # Se a rota está bloqueada, armazena em fallback_routes
                if route.bloqueado or not transport.can_access_route(route):
                    fallback_routes.append((neighbor.nome, g_cost[current] + route.temp_cost, path))
                    continue

                # Calcula o custo provisório
                tentative_g_cost = g_cost[current] + route.temp_cost
                if neighbor.nome not in g_cost or tentative_g_cost < g_cost[neighbor.nome]:
                    g_cost[neighbor.nome] = tentative_g_cost
                    f_cost = tentative_g_cost + heuristic(graph.get_node(neighbor.nome), graph.get_node(goal))
                    heappush(open_set, (f_cost, neighbor.nome, path))

    # Se nenhum caminho foi encontrado, tenta rotas bloqueadas como último recurso
    if fallback_routes:
        print("\nAviso: Rotas bloqueadas foram usadas como último recurso.")
        fallback_routes.sort(key=lambda x: x[1])  # Ordenar por menor custo
        for fallback in fallback_routes:
            neighbor, tentative_cost, path = fallback
            if neighbor not in g_cost or tentative_cost < g_cost[neighbor]:
                g_cost[neighbor] = tentative_cost
                f_cost = tentative_cost + heuristic(neighbor, goal)
                heappush(open_set, (f_cost, neighbor, path))

        # Reexecuta o A* com as rotas bloqueadas consideradas
        return a_star(graph, start, goal, heuristic, transport)

    return None, None  # Caminho não encontrado
