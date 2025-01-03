from heapq import heappush, heappop

def greedy_search(graph, start, transport, heuristic):
    """
    Implementa o algoritmo Greedy Search adaptado para percorrer todas as localidades,
    gerenciar reabastecimento e lidar com rotas bloqueadas.
    :param graph: Objeto do grafo.
    :param start: Nó inicial.
    :param transport: Objeto Transporte.
    :param heuristic: Função heurística.
    :return: Tuplo (caminho completo, custo total).
    """
    open_set = []  
    visited = set()  
    localidades_restantes = {node.nome for node in graph.nodes.values() if node.mantimentos > 0}
    caminho_completo = []  
    total_entregue = 0

    def find_nearest_reabastecimento(current_node):
        """
        Encontra o centro de reabastecimento mais próximo usando custo uniforme.
        :param current_node: Objeto Localidade atual.
        :return: Nome do reabastecimento mais próximo e custo.
        """
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

    heappush(open_set, (0, 0, start, []))  

    while open_set:
        h_cost, current_cost, current, path = heappop(open_set)
        path = path + [current]
        caminho_completo.append(current)

        if current in visited:
            continue
        visited.add(current)

        current_node = graph.get_node(current)
        if not current_node:
            continue

        if current_node.mantimentos > 0 and current in localidades_restantes:
            entrega = min(current_node.mantimentos, transport.capacidade)
            current_node.mantimentos -= entrega
            transport.carga_atual -= entrega
            total_entregue += entrega
            if current_node.mantimentos == 0:
                localidades_restantes.remove(current)
            print(f"Entregue {entrega} mantimentos em {current_node.nome}. Restam {current_node.mantimentos}.")

        if transport.autonomia <= 0 or transport.carga_atual <= 0:
            if current_node.reabastecimento:
                transport.carga_atual = transport.capacidade
                transport.autonomia = transport.autonomia
                current_cost += 3  
                print(f"Reabastecimento em {current_node.nome}: carga e autonomia restauradas.")
            else:
                nearest_reabastecimento, distancia = find_nearest_reabastecimento(current_node)
                if nearest_reabastecimento:
                    print(f"Dirigindo-se ao reabastecimento mais próximo: {nearest_reabastecimento}.")
                    heappush(open_set, (
                        h_cost,
                        current_cost + (distancia / transport.velocidade),
                        nearest_reabastecimento,
                        path + [nearest_reabastecimento]
                    ))
                continue


        if not localidades_restantes:
            print("Todas as localidades foram atendidas.")
            return caminho_completo, current_cost


        for neighbor in graph.get_neighbors(current_node):
            route = graph.get_route(current_node, neighbor)


            if route and (route.bloqueado or not transport.can_access_route(route)):
                continue

            
            if neighbor.nome not in visited:
                heappush(open_set, (
                    heuristic(graph.get_node(neighbor.nome), graph.get_node(start)),  
                    current_cost + route.temp_cost,  
                    neighbor.nome,
                    path
                ))

    return caminho_completo, current_cost
