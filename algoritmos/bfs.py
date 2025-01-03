from collections import deque
from heapq import heappop, heappush


def bfs(graph, start, transport):
    visited = set()
    queue = deque([([start], transport.capacidade, transport.autonomia, 0)])
    total_entregue = 0

    # Localidades restantes excluindo as de reabastecimento
    localidades_restantes = {
        node.nome for node in graph.nodes.values() if node.mantimentos > 0 and not node.reabastecimento
    }
    localidades_pendentes = set()
    caminho_completo = []

    def find_nearest_reabastecimento(current_node):
        pq = []
        heappush(pq, (0, current_node.nome))
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

        return None, float('inf')

    while queue:
        path, carga_atual, autonomia_restante, tempo_total = queue.popleft()
        current = path[-1]
        caminho_completo.append(current)

        current_node = graph.get_node(current)
        if not current_node:
            continue

        # Entrega de mantimentos
        if current_node.mantimentos > 0 and current in localidades_restantes:
            entrega = min(current_node.mantimentos, carga_atual)
            current_node.mantimentos -= entrega
            carga_atual -= entrega
            total_entregue += entrega

            if current_node.mantimentos == 0:
                localidades_restantes.remove(current)
                print(f"Entregue {entrega} mantimentos em {current_node.nome}. Todos atendidos.")
            else:
                localidades_pendentes.add(current)
                print(f"Entregue {entrega} mantimentos em {current_node.nome}. Ainda restam {current_node.mantimentos}.")

        # Verifica reabastecimento
        if autonomia_restante <= 0 or carga_atual == 0:
            if current_node.reabastecimento:
                carga_atual = transport.capacidade
                tempo_total += 3  # Tempo fixo para reabastecimento
                autonomia_restante = transport.autonomia
                print(f"Reabastecimento em {current_node.nome}: carga e autonomia restauradas.")
            else:
                print(f"Autonomia ou carga insuficientes em {current_node.nome}. Procurando reabastecimento...")
                nearest_reabastecimento, distance_to_reabastecimento = find_nearest_reabastecimento(current_node)
                if nearest_reabastecimento:
                    print(f"Dirigindo-se ao reabastecimento mais próximo: {nearest_reabastecimento}.")
                    tempo_total += distance_to_reabastecimento / transport.velocidade
                    queue.append((
                        path + [nearest_reabastecimento],
                        carga_atual,
                        autonomia_restante - distance_to_reabastecimento,
                        tempo_total
                    ))
                continue

        # Verificar se todas as localidades foram atendidas
        if not localidades_restantes and not localidades_pendentes:
            print("Todas as localidades foram atendidas.")
            return caminho_completo, tempo_total

        # Adicionar vizinhos à fila
        neighbors = sorted(
            graph.get_neighbors(current_node),
            key=lambda n: graph.get_node(n.nome).urgencia,
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
                    tempo_total + (route.distancia / transport.velocidade)
                ))

        # Repriorizar localidades pendentes
        for pendente in list(localidades_pendentes):
            queue.append((
                path + [pendente],
                carga_atual,
                autonomia_restante,
                tempo_total
            ))
            localidades_pendentes.remove(pendente)

    return caminho_completo, tempo_total
