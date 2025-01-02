def dfs(graph, start, goal):
    """
    Implementa o algoritmo DFS com cálculo do custo total.
    :param graph: Objeto da classe Grafo.
    :param start: Identificador do nó inicial (string).
    :param goal: Identificador do nó objetivo (string).
    :return: Tuplo (caminho, custo total) ou (None, None) se não for possível.
    """
    def dfs_recursive(current, goal, path, visited, total_cost):
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
                    if route:
                        # Explora o próximo nó recursivamente
                        result, cost = dfs_recursive(
                            neighbor.nome, goal, path, visited, total_cost + route.temp_cost
                        )
                        if result:  # Se encontrar o caminho, retorna
                            return result, cost

        # Retrocede se não encontrar o caminho
        path.pop()
        return None, None

    # Inicializa os parâmetros
    return dfs_recursive(start, goal, [], set(), 0)
