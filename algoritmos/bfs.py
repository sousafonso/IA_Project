from collections import deque
from heapq import heappop, heappush


def bfs(graph, start, transport):
    visited = set()  # Conjunto de nós visitados
    queue = deque([([start], transport.carga_atual, transport.autonomia, 0)])  # Fila com (caminho, carga, autonomia, tempo)
    total_entregue = 0  # Total de mantimentos entregues
    localidades_restantes = {node.nome for node in graph.nodes.values() if node.mantimentos > 0}  # Localidades com mantimentos
    caminho_completo = []

    def find_nearest_reabastecimento(current_node):
        """
        Encontra o centro de reabastecimento mais próximo usando BFS.
        :param current_node: Nó atual.
        :return: Nome do centro de reabastecimento mais próximo e distância.
        """
        pq = []
        heappush(pq, (0, current_node.nome))  # (distância acumulada, nó atual)
        visited_reabastecimento = set()

        while pq:
            cost, node_name = heappop(pq)
            node = graph.get_node(node_name)

            if node and node.reabastecimento and node_name not in visited_reabastecimento:
                return node_name, cost

            if node_name not in visited_reabastecimento:
                visited_reabastecimento.add(node_name)
                for neighbor in graph.get_neighbors(node):
                    route = graph.get_route(node, neighbor)
                    if route:
                        heappush(pq, (cost + route.distancia, neighbor.nome))

        return None, float('inf')  # Nenhum reabastecimento encontrado

    while queue:
        path, carga_atual, autonomia_restante, tempo_total = queue.popleft()  # Remove o caminho da frente da fila
        current = path[-1]  # Último nó no caminho atual
        caminho_completo.append(current) 

        # Localidade atual
        current_node = graph.get_node(current)
        if not current_node:
            continue

        # Entregar mantimentos
        if current_node.mantimentos > 0 and current in localidades_restantes:
            entrega = min(current_node.mantimentos, carga_atual)
            current_node.mantimentos -= entrega
            carga_atual -= entrega
            total_entregue += entrega
            localidades_restantes.remove(current) if current_node.mantimentos == 0 else None
            print(f"Entregue {entrega} mantimentos em {current_node.nome}. Restam {current_node.mantimentos}.")

        # Verificar reabastecimento antecipado
        if autonomia_restante <= 0 or carga_atual == 0:
            if current_node.reabastecimento:
                carga_atual = transport.capacidade
                autonomia_restante = transport.autonomia
                print(f"Reabastecimento em {current_node.nome}: carga e autonomia restauradas.")
            else:
                print(f"Autonomia ou carga insuficientes em {current_node.nome}. Procurando reabastecimento...")
                nearest_reabastecimento, distance_to_reabastecimento = find_nearest_reabastecimento(current_node)
                if nearest_reabastecimento:
                    print(f"Dirigindo-se ao reabastecimento mais próximo: {nearest_reabastecimento}.")
                    queue.append((
                        path + [nearest_reabastecimento],
                        carga_atual,
                        autonomia_restante - distance_to_reabastecimento,
                        tempo_total + (distance_to_reabastecimento / transport.velocidade)
                    ))
                continue

        # Verificar se todas as localidades foram atendidas
        if not localidades_restantes:
            print("Todas as localidades foram atendidas.")
            return caminho_completo, tempo_total

        # Adicionar vizinhos à fila
        neighbors = sorted(
            graph.get_neighbors(current_node),
            key=lambda n: graph.get_node(n.nome).urgencia,  # Ordenar por urgência
            reverse=True
        )
        for neighbor in neighbors:
            route = graph.get_route(current_node, neighbor)
            if neighbor.nome not in visited and route:
                visited.add(neighbor.nome)
                queue.append((
                    path + [neighbor.nome],
                    carga_atual,
                    autonomia_restante - route.distancia,
                    tempo_total + (route.distancia / transport.velocidade)  # Adicionar tempo da rota
                ))

    return caminho_completo, tempo_total
