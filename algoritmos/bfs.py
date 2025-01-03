from collections import deque

def bfs(graph, start, goal, transport):
    """
    Implementa o algoritmo BFS para encontrar o menor caminho entre dois nós e calcular o custo total.
    Se uma rota está bloqueada, tenta encontrar caminhos alternativos.
    :param graph: Objeto da classe Grafo.
    :param start: Identificador do nó inicial (string).
    :param goal: Identificador do nó objetivo (string).
    :param transport: Objeto Transporte, que define o tipo de transporte usado.
    :return: Tuplo (caminho, custo total) ou (None, None) se não for possível.
    """
    visited = set()  # Conjunto de nós visitados
    queue = deque([([start], 0)])  # Fila que contém caminhos e seus custos ([(caminho, custo)])
    fallback_routes = []  # Lista para armazenar rotas bloqueadas que podem ser usadas como último recurso

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

                    # Verifica se a rota está bloqueada ou é inacessível para o transporte
                    if route.bloqueado or not transport.can_access_route(route):
                        fallback_routes.append((path + [neighbor.nome], total_cost + route.temp_cost))
                        continue

                    # Adiciona o vizinho ao caminho
                    new_path = path + [neighbor.nome]
                    queue.append((new_path, total_cost + route.temp_cost))

    # Se nenhum caminho foi encontrado, tenta usar rotas bloqueadas como último recurso
    if fallback_routes:
        print("\nAviso: Rotas bloqueadas foram usadas como último recurso.")
        fallback_routes.sort(key=lambda x: x[1])  # Ordenar por menor custo
        return fallback_routes[0]  # Retorna o caminho com menor custo entre as alternativas

    return None, None  # Caminho não encontrado
