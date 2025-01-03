from heapq import heappop, heappush

def uniform_cost_search(graph, start, transport):
    caminho_completo = []
    total_entregue = 0
    localidades_restantes = {node.nome for node in graph.nodes.values() if node.mantimentos > 0}
    priority_queue = [(0, start, transport.capacidade, transport.autonomia, [])]
    localidades_pendentes = set()

    def find_nearest_reabastecimento(current_node):
        pq = [(0, current_node.nome)]
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

    while priority_queue:
        custo_atual, current, carga_atual, autonomia_restante, path = heappop(priority_queue)
        path = path + [current]

        current_node = graph.get_node(current)
        if not current_node or (current in caminho_completo and current not in localidades_restantes):
            continue


        if not caminho_completo or caminho_completo[-1] != current:
            caminho_completo.append(current)


        if current_node.mantimentos > 0 and carga_atual > 0:
            entrega = min(current_node.mantimentos, carga_atual)
            current_node.mantimentos -= entrega
            carga_atual -= entrega
            total_entregue += entrega
            print(f"Entregue {entrega} mantimentos em {current_node.nome}. Restante: {current_node.mantimentos}.")
            if current_node.mantimentos == 0:
                localidades_restantes.remove(current)
            else:
                localidades_pendentes.add(current)


        if autonomia_restante <= 0 or carga_atual <= 0:
            nearest_reabastecimento, distancia = find_nearest_reabastecimento(current_node)
            if nearest_reabastecimento:
                print(f"Dirigindo-se ao reabastecimento mais próximo: {nearest_reabastecimento}.")
                custo_atual += (distancia / transport.velocidade) + 3
                carga_atual = transport.capacidade
                autonomia_restante = transport.autonomia
                caminho_completo.append(nearest_reabastecimento)
                print(f"Reabastecimento em {nearest_reabastecimento}: carga e autonomia restauradas.")
                heappush(priority_queue, (
                    custo_atual,
                    current,
                    carga_atual,
                    autonomia_restante,
                    path
                ))
                continue


        if not localidades_restantes and not localidades_pendentes:
            print("Todas as localidades foram atendidas.")
            return caminho_completo, custo_atual


        neighbors = graph.get_neighbors(current_node)
        for neighbor in neighbors:
            route = graph.get_route(current_node, neighbor)
            if route and transport.can_access_route(route):
                nova_autonomia = autonomia_restante - route.distancia
                novo_custo = custo_atual + (route.distancia / transport.velocidade)
                heappush(priority_queue, (
                    novo_custo,
                    neighbor.nome,
                    carga_atual,
                    nova_autonomia,
                    path
                ))

        while localidades_pendentes:
            pendente = localidades_pendentes.pop()
            heappush(priority_queue, (
                custo_atual,
                pendente,
                carga_atual,
                autonomia_restante,
                path
            ))

    return caminho_completo, custo_atual
