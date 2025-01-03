from heapq import heappush, heappop

def uniform_cost_search(graph, start, goal, transport):
    """
    Implementa o algoritmo de Custo Uniforme.
    Caso uma rota esteja bloqueada, tenta encontrar caminhos alternativos.
    :param graph: Objeto Grafo.
    :param start: Nó inicial.
    :param goal: Nó objetivo.
    :param transport: Objeto Transporte.
    :return: Tuplo (caminho, tempo total) ou (None, None) se não for possível.
    """
    priority_queue = []  # (tempo acumulado, nó atual, caminho)
    heappush(priority_queue, (0, start, []))
    visited = set()
    fallback_routes = []  # Lista para rotas bloqueadas

    while priority_queue:
        time, current, path = heappop(priority_queue)  # Nó com menor tempo acumulado
        path = path + [current]  # Atualiza o caminho

        if current == goal:
            return path, time  # Caminho encontrado com tempo total

        if current not in visited:
            visited.add(current)  # Marca o nó como visitado
            current_node = graph.get_node(current)  # Obter o nó atual

            for neighbor in graph.get_neighbors(current_node):
                route = graph.get_route(current_node, neighbor)

                # Se a rota está bloqueada, adiciona aos caminhos alternativos
                if route.bloqueado or not transport.can_access_route(route):
                    fallback_routes.append((time + route.calculate_time(transport.velocidade), neighbor.nome, path))
                    continue

                # Adiciona a rota acessível na fila de prioridades
                heappush(priority_queue, (time + route.calculate_time(transport.velocidade), neighbor.nome, path))

    # Caso nenhuma rota acessível encontre o objetivo, tenta rotas bloqueadas
    if fallback_routes:
        print("\nAviso: Rotas bloqueadas foram usadas como último recurso.")
        fallback_routes.sort(key=lambda x: x[0])  # Ordenar por tempo acumulado
        for fallback_time, fallback_node, fallback_path in fallback_routes:
            heappush(priority_queue, (fallback_time, fallback_node, fallback_path))

        # Reexecuta o Uniform Cost Search com as rotas bloqueadas adicionadas
        return uniform_cost_search(graph, start, goal, transport)

    return None, None  # Caminho não encontrado
