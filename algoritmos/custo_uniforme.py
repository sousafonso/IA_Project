from heapq import heappush, heappop

def uniform_cost_search(graph, start, goal):
    """
    Implementa o algoritmo de Custo Uniforme (UCS) com base no custo temporário (tempo de viagem).
    :param graph: Objeto da classe Grafo.
    :param start: Identificador do nó inicial (string).
    :param goal: Identificador do nó objetivo (string).
    :return: Tuplo (caminho, custo total) ou (None, None) se não for possível.
    """
    priority_queue = []  # Fila de prioridade contendo (custo acumulado, nó atual, caminho)
    heappush(priority_queue, (0, start, []))  # Adiciona o nó inicial à fila
    visited = set()  # Conjunto de nós já visitados

    while priority_queue:
        cost, current, path = heappop(priority_queue)  # Nó com menor custo
        path = path + [current]  # Atualiza o caminho

        if current == goal:
            return path, cost  # Caminho e custo encontrados

        if current not in visited:
            visited.add(current)  # Marca o nó como visitado
            current_node = graph.get_node(current)  # Obter o nó atual

            if current_node:
                for neighbor in graph.get_neighbors(current_node):  # Explorar vizinhos
                    route = graph.get_route(current_node, neighbor)  # Obter a rota
                    if route and not route.bloqueado:  # Verificar se a rota não está bloqueada
                        # Adicionar o vizinho à fila com o custo atualizado (tempo de viagem)
                        heappush(priority_queue, (cost + route.temp_cost, neighbor.nome, path))

    return None, None  # Caminho não encontrado
