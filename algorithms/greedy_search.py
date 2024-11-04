#Desenvolver um sistema que utilize algoritmos de procura para otimizar a distribuição de suprimentos 
# (alimentos, água, medicamentos) em zonas afetadas por uma catástrofe natural. O sistema deve garantir a 
# eficiência no uso dos recursos e priorizar as áreas mais necessitadas, maximizando a assistência no menor tempo possível.

# Contém a implementação do algoritmo de procura gulosa, que foca em expandir o nó mais promissor de acordo com uma heurística.

def greedy_search(graph, start, goal, heuristic):
    # Inicializa a lista de nós a serem visitados com o nó inicial
    open_list = [start]
    # Inicializa a lista de nós visitados
    closed_list = []
    # Inicializa o dicionário de custos acumulados
    costs = {start: 0}
    # Inicializa o dicionário de nós predecessores
    predecessors = {start: None}

    # Enquanto houver nós a serem visitados
    while open_list:
        # Seleciona o nó mais promissor
        current = min(open_list, key=lambda node: costs[node] + heuristic(node, goal))
        # Se o nó for o objetivo, retorna o caminho até ele
        if current == goal:
            path = []
            while current is not None:
                path.insert(0, current)
                current = predecessors[current]
            return path
        # Remove o nó da lista de abertos
        open_list.remove(current)
        # Adiciona o nó à lista de fechados
        closed_list.append(current)
        # Para cada vizinho do nó
        for neighbor, distance in graph.get_neighbors(current):
            # Se o vizinho já foi visitado, ignora
            if neighbor in closed_list:
                continue
            # Calcula o custo acumulado até o vizinho
            new_cost = costs[current] + distance
            # Se o vizinho não está na lista de abertos, adiciona
            if neighbor not in open_list:
                open_list.append(neighbor)
            # Se o novo custo for menor que o custo atual, atualiza
            if neighbor not in costs or new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                predecessors[neighbor] = current