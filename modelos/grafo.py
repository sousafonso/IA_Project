from modelos.rota import Rota
from modelos.localidade import Localidade

class Grafo:
    def __init__(self):
        self.nodes = {}  
        self.edges = {}

    def add_node(self, locality):
        self.nodes[locality.nome] = locality

    def add_edge(self, origem, destino, distancia, pavimento, restricoes=None):
        route = Rota(f"{origem}-{destino}", origem, destino, distancia, pavimento, restricoes)
        self.edges[(origem, destino)] = route

    def get_node(self, nome):
        """
        Obtém uma localidade pelo seu identificador.
        :param id: Identificador da localidade.
        :return: Objeto Localidade.
        """
        return self.nodes.get(nome)
    
    def get_neighbors(self, node):
        """
        Retorna os vizinhos de um nó.
        :param node: Objeto da classe Localidade.
        :return: Lista de objetos Localidade que são vizinhos.
        """
        neighbors = []
        for (origin, destination), route in self.edges.items():
            if origin == node.id and not route.blocked:  # Verifica se a rota não está bloqueada
                neighbors.append(self.nodes[destination])
        return neighbors

    def display(self):
        print("\nGrafo de Localidades e Rotas:")
        for node in self.nodes.values():
            print(node)
        for route in self.edges.values():
            print(f"Rota de {route.origem} para {route.destino}, Distância: {route.distancia} km, Pavimento: {route.pavimento}, Bloqueada: {route.bloqueado}")
