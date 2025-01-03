from heapq import heappush, heappop
from modelos.transporte import Transporte

def a_star(graph, start, heuristic, transport):
    open_set = []  
    heappush(open_set, (0, start, transport.capacidade, transport.autonomia, []))  

    g_cost = {start: 0}  
    visited = set()  
    localidades_restantes = {node.nome for node in graph.nodes.values() if node.mantimentos > 0 and not node.reabastecimento}
    localidades_pendentes = set()  
    caminho_completo = []  
    total_entregue = 0

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
        f_cost, current, carga_atual, autonomia_restante, path = heappop(open_set)
        path = path + [current]
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
                f_cost += 3  
                print(f"Reabastecimento em {current_node.nome}: carga e autonomia restauradas.")

                # Retornar às localidades pendentes após reabastecimento
                if current in localidades_pendentes:
                    localidades_pendentes.remove(current)
                    heappush(open_set, (
                        f_cost,
                        current,
                        carga_atual,
                        autonomia_restante,
                        path
                    ))
            else:
                nearest_reabastecimento, distancia = find_nearest_reabastecimento(current_node)
                if nearest_reabastecimento:
                    print(f"Dirigindo-se ao reabastecimento mais próximo: {nearest_reabastecimento}.")
                    heappush(open_set, (
                        f_cost + (distancia / transport.velocidade),
                        nearest_reabastecimento,
                        carga_atual,
                        autonomia_restante - distancia,
                        path + [nearest_reabastecimento]
                    ))
                continue

        # Verificar se todas as localidades foram atendidas
        if not localidades_restantes and not localidades_pendentes:
            print("Todas as localidades foram atendidas.")
            return caminho_completo, f_cost

        # Adicionar vizinhos à fila
        for neighbor in graph.get_neighbors(current_node):
            route = graph.get_route(current_node, neighbor)

            if route and (route.bloqueado or not transport.can_access_route(route)):
                continue

            tentative_g_cost = g_cost.get(current, float('inf')) + route.temp_cost
            if neighbor.nome not in g_cost or tentative_g_cost < g_cost[neighbor.nome]:
                g_cost[neighbor.nome] = tentative_g_cost
                heuristic_cost = heuristic(graph.get_node(neighbor.nome), graph.get_node(start))
                heappush(open_set, (
                    tentative_g_cost + heuristic_cost,
                    neighbor.nome,
                    carga_atual,
                    autonomia_restante - route.distancia,
                    path
                ))

        # Retornar às localidades pendentes
        while localidades_pendentes:
            pendente = localidades_pendentes.pop()
            g_cost[pendente] = g_cost.get(pendente, float('inf'))  # Inicializar g_cost se necessário
            heappush(open_set, (
                f_cost,
                pendente,
                carga_atual,
                autonomia_restante,
                path + [pendente]
            ))

    return caminho_completo, f_cost
