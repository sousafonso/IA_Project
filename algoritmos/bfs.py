from collections import deque

def bfs(graph, start, goal):
    """
    Implementa o algoritmo BFS para encontrar o menor caminho entre dois nós.
    :param graph: Objeto da classe Grafo.
    :param start: Identificador do nó inicial (string).
    :param goal: Identificador do nó objetivo (string).
    :return: Lista representando o caminho do início ao objetivo, ou None se não for possível.
    """
    visited = set()  # Conjunto de nós já visitados
    queue = deque([[start]])  # Fila que contém caminhos em vez de nós únicos

    while queue:
        path = queue.popleft()  # Obtém o caminho da frente da fila
        node_id = path[-1]  # Último nó no caminho atual

        if node_id == goal:
            return path  # Caminho encontrado

        if node_id not in visited:
            visited.add(node_id)
            # Obter o nó atual e seus vizinhos
            current_node = graph.get_node(node_id)
            if current_node:
                for neighbor in graph.get_neighbors(current_node):
                    new_path = list(path)  # Cria um novo caminho baseado no atual
                    new_path.append(neighbor.nome)  # Adiciona o vizinho ao caminho
                    queue.append(new_path)

    return None  # Caminho não encontrado
