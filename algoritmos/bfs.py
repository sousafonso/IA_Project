from collections import deque

def bfs(graph, start, goal, transport):
    """
    Implementa o algoritmo BFS para encontrar o menor caminho entre dois nós e calcular o custo total.
    :param graph: Objeto da classe Grafo.
    :param start: Identificador do nó inicial (string).
    :param goal: Identificador do nó objetivo (string).
    :return: Tuplo (caminho, custo total) ou (None, None) se não for possível.
    """
    visited = set()  # Conjunto de nós visitados
    queue = deque([([start], 0)])  # Fila que contém caminhos e seus custos ([(caminho, custo)])

    while queue:
        path, total_cost = queue.popleft()  # Remove o caminho da frente da fila
        node_id = path[-1]  # Último nó no caminho atual

        if node_id == goal:
            return path, total_cost  # Caminho e custo encontrados

        if node_id not in visited:
            visited.add(node_id)  # Marca o nó como visitado
            current_node = graph.get_node(node_id)  # Obtém o nó atual
            if current_node:
                for neighbor in graph.get_neighbors(current_node):  # Obter vizinhos
                    route = graph.get_route(current_node, neighbor)  # Obtém a rota
                    if route.bloqueado and not transport.can_access_route(route):
                        continue  # ignorar rotas inacessíveis
                    new_path = path + [neighbor.nome]  # Adiciona o vizinho ao caminho
                    queue.append((new_path, total_cost + route.distancia))  # Soma o custo da rota

    return None, None  # Caminho não encontrado
