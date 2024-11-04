#Desenvolver um sistema que utilize algoritmos de procura para otimizar a distribuição de suprimentos 
# (alimentos, água, medicamentos) em zonas afetadas por uma catástrofe natural. O sistema deve garantir a 
# eficiência no uso dos recursos e priorizar as áreas mais necessitadas, maximizando a assistência no menor tempo possível.

# Implementa o algoritmo A*, que é uma procura informada que utiliza uma função heurística para encontrar o caminho mais eficiente.

def a_star(graph, start, goal):
    open_set = set([start])
    closed_set = set()
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, goal)
    
    while open_set:
        current = min(open_set, key=lambda node: f_score[node])
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path
        
        open_set.remove(current)
        closed_set.add(current)
        
        for neighbor in graph[current]:
            if neighbor in closed_set:
                continue
            
            tentative_g_score = g_score[current] + graph[current][neighbor]
            
            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue
            
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
    
    return None