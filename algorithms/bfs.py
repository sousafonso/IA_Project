#Desenvolver um sistema que utilize algoritmos de procura para otimizar a distribuição de suprimentos 
# (alimentos, água, medicamentos) em zonas afetadas por uma catástrofe natural. O sistema deve garantir a 
# eficiência no uso dos recursos e priorizar as áreas mais necessitadas, maximizando a assistência no menor tempo possível.

# Contém a implementação do algoritmo de procura em largura (Breadth-First Search), utilizado para explorar todas as rotas em um nível antes de passar para o próximo.

from queue import Queue

from models.graph import Graph
from models.locality import Locality
from models.route import Route
from models.transport import Transport
from models.supply import Supply

def bfs(graph: Graph, start: Locality, goal: Locality, transport: Transport):
    # Inicializa a fila
    frontier = Queue()
    frontier.put(start)
    
    # Inicializa o caminho
    came_from = {start: None}
    
    # Enquanto houver localidades na fila
    while not frontier.empty():
        current = frontier.get()
        
        # Se a localidade atual for o objetivo, termina
        if current == goal:
            break
        
        # Para cada localidade adjacente
        for next in graph.neighbors(current):
            # Se a localidade não foi visitada
            if next not in came_from:
                # Adiciona a localidade à fila
                frontier.put(next)
                
                # Atualiza o caminho
                came_from[next] = current
    
    # Reconstrói o caminho
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path