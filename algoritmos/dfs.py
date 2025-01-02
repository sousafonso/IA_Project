def dfs(graph, start, goal, path=None, visited=None):
    """
    Implementa o algoritmo DFS com melhorias.
    :param graph: Dicionário representando o grafo {nó: [vizinhos]}.
    :param start: Nó inicial.
    :param goal: Nó objetivo.
    :param path: Caminho atual (usado internamente na recursão).
    :param visited: Conjunto de nós visitados.
    :return: Lista representando o caminho do início ao objetivo, ou None se não for possível.
    """
    if path is None:
        path = []
    if visited is None:
        visited = set()

    path.append(start)
    visited.add(start)

    if start == goal:
        return path  # Caminho encontrado

    for neighbor, _ in graph.get(start, []):
        if neighbor not in visited:
            result = dfs(graph, neighbor, goal, path, visited)
            if result:
                return result

    path.pop()  # Retrocede
    return None  # Caminho não encontrado
    