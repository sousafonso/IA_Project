from heapq import heappush, heappop

def a_star(graph, start, heuristic, transport):
    open_set = []
    heappush(open_set, (0, 0, start, transport.capacidade, transport.autonomia, 0, []))  

    localidades_restantes = {node.nome for node in graph.nodes.values() if node.mantimentos > 0}
    localidades_pendentes = set()
    caminho_completo = []
    atendidos = set() 

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

    while open_set:
        f_cost, g_cost_current, current, carga_atual, autonomia_restante, tempo_total, path = heappop(open_set)
        path = path + [current]

        if not caminho_completo or caminho_completo[-1] != current:
            caminho_completo.append(current)

        current_node = graph.get_node(current)
        if not current_node:
            continue


        if current_node.mantimentos > 0:
            entrega = min(current_node.mantimentos, carga_atual)
            current_node.mantimentos -= entrega
            carga_atual -= entrega
            print(f"Foram entregues {entrega} mantimentos em {current_node.nome}. Restam entregar: {current_node.mantimentos}.")
            if current_node.mantimentos == 0:
                localidades_restantes.remove(current)
                atendidos.add(current)
            else:
                localidades_pendentes.add(current)


        if autonomia_restante <= 0 or carga_atual <= 0:
            if current_node.reabastecimento:
                carga_atual = transport.capacidade
                autonomia_restante = transport.autonomia
                tempo_total += 3 
                print(f"Reabastecimento em {current_node.nome}: .")
            else:
                nearest_reabastecimento, distancia = find_nearest_reabastecimento(current_node)
                if nearest_reabastecimento:
                    print(f"A dirigir ao abastecimento: {nearest_reabastecimento}.")
                    tempo_total += distancia / transport.velocidade
                    heappush(open_set, (
                        g_cost_current + distancia + heuristic(graph.get_node(nearest_reabastecimento), None),
                        g_cost_current + distancia,
                        nearest_reabastecimento,
                        carga_atual,
                        autonomia_restante - distancia,
                        tempo_total,
                        path + [nearest_reabastecimento]
                    ))
                continue


        if not localidades_restantes and not localidades_pendentes:
            print("Todas as localidades foram atendidas.")
            return caminho_completo, tempo_total

        for neighbor in graph.get_neighbors(current_node):
            if neighbor.nome in atendidos: 
                continue
            route = graph.get_route(current_node, neighbor)
            if route and transport.can_access_route(route):
                tentative_g_cost = g_cost_current + route.distancia
                heuristic_cost = heuristic(graph.get_node(neighbor.nome), None)
                heappush(open_set, (
                    tentative_g_cost + heuristic_cost,
                    tentative_g_cost,
                    neighbor.nome,
                    carga_atual,
                    autonomia_restante - route.distancia,
                    tempo_total + (route.distancia / transport.velocidade),
                    path
                ))


        for pendente in list(localidades_pendentes):
            if pendente in atendidos:  
                localidades_pendentes.remove(pendente)
                continue
            heappush(open_set, (
                g_cost_current + heuristic(graph.get_node(pendente), None),
                g_cost_current,
                pendente,
                carga_atual,
                autonomia_restante,
                tempo_total,
                path
            ))
            localidades_pendentes.remove(pendente)

    return caminho_completo, float('inf')  
