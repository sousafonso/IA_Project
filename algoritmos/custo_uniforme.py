from heapq import heappush, heappop

def uniform_cost_search(graph, start, goal, transport=None):
    priority_queue = []  # Fila de prioridade (custo acumulado, nó atual, caminho)
    heappush(priority_queue, (0, start, []))
    visited = set()

    while priority_queue:
        cost, current, path = heappop(priority_queue)
        path = path + [current]

        if current == goal:
            return path  # Caminho encontrado

        if current not in visited:
            visited.add(current)

            # Explorar vizinhos do nó atual
            for neighbor, neighbor_cost, is_blocked in graph.get(current, []):
                # Verificar se a rota está bloqueada
                if is_blocked:
                    continue

                # Verificar restrições de transporte
                if transport and not transport.can_access_route(neighbor):
                    continue

                # Adicionar vizinho à fila com o custo acumulado atualizado
                heappush(priority_queue, (cost + neighbor_cost, neighbor, path))

    return None  # Caminho não encontrado
