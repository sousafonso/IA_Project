def dfs(graph, start, goal, transport, path=None, visited=None):
    """
    Implementa o algoritmo DFS com cálculo do custo total.
    Caso uma rota esteja bloqueada, tenta encontrar caminhos alternativos.
    :param graph: Objeto da classe Grafo.
    :param start: Identificador do nó inicial (string).
    :param goal: Identificador do nó objetivo (string).
    :param transport: Objeto Transporte, que define o tipo de transporte usado.
    :return: Tuplo (caminho, custo total) ou (None, None) se não for possível.
    """
    def dfs_recursive(current, goal, path, visited, total_cost, fallback_routes):
        # Adiciona o nó atual ao caminho
        path.append(current)
        visited.add(current)

        # Verifica se o nó objetivo foi alcançado
        if current == goal:
            return path, total_cost  # Caminho e custo encontrados

        current_node = graph.get_node(current)
        if current_node:
            for neighbor in graph.get_neighbors(current_node):  # Obter vizinhos
                if neighbor.nome not in visited:
                    route = graph.get_route(current_node, neighbor)  # Obter a rota para o vizinho
                    if route.bloqueado or not transport.can_access_route(route):
                        # Adiciona a rota bloqueada como alternativa
                        fallback_routes.append((neighbor.nome, total_cost + route.temp_cost))
                        continue

                    # Explora o próximo nó recursivamente
                    result, cost = dfs_recursive(
                        neighbor.nome, goal, path, visited, total_cost + route.temp_cost, fallback_routes
                    )
                    if result:  # Se encontrar o caminho, retorna
                        return result, cost

        # Retrocede se não encontrar o caminho
        path.pop()
        return None, None

    # Inicializa os parâmetros
    fallback_routes = []  # Lista para rotas bloqueadas
    result, cost = dfs_recursive(start, goal, [], set(), 0, fallback_routes)

    # Se nenhum caminho foi encontrado, tenta usar rotas bloqueadas
    if not result and fallback_routes:
        print("\nAviso: Rotas bloqueadas foram usadas como último recurso.")
        for fallback in fallback_routes:
            fallback_path, fallback_cost = dfs_recursive(
                fallback[0], goal, [], set(), fallback[1], []
            )
            if fallback_path:
                return fallback_path, fallback_cost

    return result, cost
