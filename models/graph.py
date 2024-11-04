#Desenvolver um sistema que utilize algoritmos de procura para otimizar a distribuição de suprimentos 
# (alimentos, água, medicamentos) em zonas afetadas por uma catástrofe natural. O sistema deve garantir a 
# eficiência no uso dos recursos e priorizar as áreas mais necessitadas, maximizando a assistência no menor tempo possível.

# Contém a classe Graph, responsável por modelar as zonas e os caminhos entre elas em forma de grafo, permitindo a representação das rotas de entrega.

def add_node(self, zone):
    if zone not in self.nodes:
        self.nodes.append(zone)
        self.edges[zone] = []


def add_edge(self, zone1, zone2, distance):
    self.edges[zone1].append((zone2, distance))
    self.edges[zone2].append((zone1, distance))

def get_neighbors(self, zone):
    return self.edges[zone]

