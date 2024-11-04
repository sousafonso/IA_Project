#Desenvolver um sistema que utilize algoritmos de procura para otimizar a distribuição de suprimentos 
# (alimentos, água, medicamentos) em zonas afetadas por uma catástrofe natural. O sistema deve garantir a 
# eficiência no uso dos recursos e priorizar as áreas mais necessitadas, maximizando a assistência no menor tempo possível.

# Contém a implementação do algoritmo de procura em largura (Breadth-First Search), utilizado para explorar todas as rotas em um nível antes de passar para o próximo.

def bfs(graph, start, goal):
    explored = []
    queue = [[start]]
    
    if start == goal:
        return "Você já está no seu destino."
    
    while queue:
        path = queue.pop(0)
        node = path[-1]
        
        if node not in explored:
            neighbours = graph[node]
            
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                
                if neighbour == goal:
                    return new_path
            
            explored.append(node)
    
    return "Não existe caminho entre o ponto de partida e o destino."