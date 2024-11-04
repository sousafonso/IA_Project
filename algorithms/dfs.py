#Desenvolver um sistema que utilize algoritmos de procura para otimizar a distribuição de suprimentos 
# (alimentos, água, medicamentos) em zonas afetadas por uma catástrofe natural. O sistema deve garantir a 
# eficiência no uso dos recursos e priorizar as áreas mais necessitadas, maximizando a assistência no menor tempo possível.

# Implementa o algoritmo de procura em profundidade (Depth-First Search), que explora cada caminho até o final antes de retroceder e tentar outras opções.

def dfs(graph, start, goal) :
    explored = []
    stack = [[start]]
    
    if start == goal:
        return "Você já está no seu destino."
    
    while stack:
        path = stack.pop()
        node = path[-1]
        
        if node not in explored:
            neighbours = graph[node]
            
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                stack.append(new_path)
                
                if neighbour == goal:
                    return new_path
            
            explored.append(node)
    
    return "Não existe caminho entre o ponto de partida e o destino."