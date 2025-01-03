def dfs(graph, start, transport):
    caminho_completo = []  
    total_entregue = 0  
    localidades_restantes = {node.nome for node in graph.nodes.values() if node.mantimentos > 0 and not node.reabastecimento}
    localidades_pendentes = set()  # Localidades que ainda precisam de entregas

    def find_nearest_reabastecimento(current_node):
        visited_reabastecimento = set()
        stack = [(current_node.nome, 0)]  

        while stack:
            node_name, cost = stack.pop()
            node = graph.get_node(node_name)

            if node and node.reabastecimento and node_name not in visited_reabastecimento:
                return node_name, cost

            if node_name not in visited_reabastecimento:
                visited_reabastecimento.add(node_name)
                for neighbor in graph.get_neighbors(node):
                    route = graph.get_route(node, neighbor)
                    if route:
                        stack.append((neighbor.nome, cost + route.distancia))

        return None, float('inf')  

    def dfs_recursive(current, carga_atual, autonomia_restante, tempo_total, visited):
        nonlocal caminho_completo, total_entregue

        caminho_completo.append(current)

        current_node = graph.get_node(current)
        if not current_node:
            return tempo_total  

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

        # Reabastecimento se necessário
        if autonomia_restante <= 0 or carga_atual <= 0:
            nearest_reabastecimento, distancia = find_nearest_reabastecimento(current_node)
            if nearest_reabastecimento:
                print(f"Dirigindo-se ao reabastecimento mais próximo: {nearest_reabastecimento}.")
                tempo_total += (distancia / transport.velocidade) + 3
                carga_atual = transport.capacidade
                autonomia_restante = transport.autonomia
                caminho_completo.append(nearest_reabastecimento)
                print(f"Reabastecimento em {nearest_reabastecimento}: carga e autonomia restauradas.")

                # Retornar às localidades pendentes
                if current in localidades_pendentes:
                    localidades_pendentes.remove(current)
                    return dfs_recursive(current, carga_atual, autonomia_restante, tempo_total, visited)
            else:
                print(f"Não foi possível encontrar reabastecimento a partir de {current}.")
                return tempo_total

        # Verificar se todas as localidades foram atendidas
        if not localidades_restantes and not localidades_pendentes:
            print("Todas as localidades foram atendidas.")
            return tempo_total

        # Explorar vizinhos
        visited.add(current)
        neighbors = sorted(
            graph.get_neighbors(current_node),
            key=lambda n: graph.get_node(n.nome).urgencia,  
            reverse=True
        )
        for neighbor in neighbors:
            route = graph.get_route(current_node, neighbor)
            if neighbor.nome not in visited and route:
                if route.bloqueado or not transport.can_access_route(route):
                    print(f"Rota bloqueada ou inacessível: {current} -> {neighbor.nome}. Buscando alternativas.")
                    continue

                nova_autonomia = autonomia_restante - route.distancia
                novo_tempo = tempo_total + (route.distancia / transport.velocidade)
                tempo_final = dfs_recursive(neighbor.nome, carga_atual, nova_autonomia, novo_tempo, visited)
                tempo_total = max(tempo_total, tempo_final)

        # Retornar às localidades pendentes após explorar os vizinhos
        while localidades_pendentes:
            pendente = localidades_pendentes.pop()
            return dfs_recursive(pendente, carga_atual, autonomia_restante, tempo_total, visited)

        return tempo_total

    visited = set()
    tempo_total = dfs_recursive(start, transport.capacidade, transport.autonomia, 0, visited)
    return caminho_completo, tempo_total
