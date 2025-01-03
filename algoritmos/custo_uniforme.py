from heapq import heappop, heappush

def uniform_cost_search(graph, start, transport):
    caminho_completo = []  
    total_entregue = 0  
    localidades_restantes = {node.nome for node in graph.nodes.values() if node.mantimentos > 0 and not node.reabastecimento} 
    localidades_pendentes = set()  # Localidades que ainda precisam de entregas
    priority_queue = [(0, start, transport.carga_atual, transport.autonomia, [])]  
    visited = set()  

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
        caminho_completo.append(current)

        if current in visited:
            continue
        visited.add(current)

        current_node = graph.get_node(current)
        if not current_node:
            continue

        # Entregar mantimentos
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

        # Verificar reabastecimento
        if autonomia_restante <= 0 or carga_atual <= 0:
            if current_node.reabastecimento:
                carga_atual = transport.capacidade
                autonomia_restante = transport.autonomia
                custo_atual += 3  # Tempo fixo para reabastecimento
                print(f"Reabastecimento em {current_node.nome}: carga e autonomia restauradas.")

                # Retornar às localidades pendentes após reabastecimento
                if current in localidades_pendentes:
                    localidades_pendentes.remove(current)
                    heappush(priority_queue, (
                        custo_atual,
                        current,
                        carga_atual,
                        autonomia_restante,
                        path
                    ))
            else:
                nearest_reabastecimento, distancia = find_nearest_reabastecimento(current_node)
                if nearest_reabastecimento:
                    print(f"Dirigindo-se ao reabastecimento mais próximo: {nearest_reabastecimento}.")
                    heappush(priority_queue, (
                        custo_atual + (distancia / transport.velocidade),
                        nearest_reabastecimento,
                        carga_atual,
                        autonomia_restante - distancia,
                        path + [nearest_reabastecimento]
                    ))
                continue

        # Verificar se todas as localidades foram atendidas
        if not localidades_restantes and not localidades_pendentes:
            print("Todas as localidades foram atendidas.")
            return caminho_completo, custo_atual

        # Adicionar vizinhos à fila
        neighbors = graph.get_neighbors(current_node)
        for neighbor in neighbors:
            route = graph.get_route(current_node, neighbor)
            if route and transport.can_access_route(route) and neighbor.nome not in visited:
                nova_autonomia = autonomia_restante - route.distancia
                novo_custo = custo_atual + (route.distancia / transport.velocidade)
                heappush(priority_queue, (
                    novo_custo,
                    neighbor.nome,
                    carga_atual,
                    nova_autonomia,
                    path + [neighbor.nome]
                ))

        # Retornar às localidades pendentes
        while localidades_pendentes:
            pendente = localidades_pendentes.pop()
            heappush(priority_queue, (
                custo_atual,
                pendente,
                carga_atual,
                autonomia_restante,
                path + [pendente]
            ))

    return caminho_completo, custo_atual
