from heapq import heappush, heappop

def greedy_search(graph, start, goal, heuristic):
    """
    Implementa o algoritmo Greedy Search com cálculo baseado na heurística.
    :param graph: Objeto da classe Grafo.
    :param start: Identificador do nó inicial (string).
    :param goal: Identificador do nó objetivo (string).
    :param heuristic: Função heurística que estima o custo até o objetivo.
    :return: Tuplo (caminho, custo total) ou (None, None) se não for possível.
    """
    open_set = []
    visited = set()
    heappush(open_set, (heuristic(start, goal), start, []))  # (valor heurístico, nó atual, caminho)

    while open_set:
        _, current, path = heappop(open_set)
        path = path + [current]

        if current == goal:
            return path  # Caminho encontrado

        if current in visited:
            continue

        visited.add(current)

        current_node = graph.get_node(current)  # Obter o nó atual
        if current_node:
            for neighbor in graph.get_neighbors(current_node):  # Explorar vizinhos
                route = graph.get_route(current_node, neighbor)  # Obter a rota
                if route and not route.bloqueado:  # Ignorar rotas bloqueadas
                    if neighbor.nome not in visited:
                        heappush(open_set, (heuristic(neighbor, graph.get_node(goal)), neighbor.nome, path))

    return None  # Caminho não encontrado
