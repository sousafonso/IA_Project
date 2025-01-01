from modelos.rota import Rota
from modelos.localidade import Localidade

class Grafo:
    def __init__(self):
        self.nodes = {}  
        self.edges = {}

    def add_node(self, locality):
        """
        Adiciona uma localidade ao grafo.
        """
        self.nodes[locality.id] = locality

    def add_edge(self, origin, destination, distance, type_pavement, restrictions=None):
        """
        Adiciona uma rota ao grafo.
        :param origin: Localidade de origem.
        :param destination: Localidade de destino.
        :param distance: Distância entre as localidades.
        :param type_pavement: Tipo de pavimento.
        :param restrictions: Lista de restrições de acesso.
        """
        route = Rota(f"{origin}-{destination}", origin, destination, distance, type_pavement, restrictions)
        self.edges[(origin, destination)] = route

    def display(self):
        """
        Exibe o grafo em formato textual.
        """
        print("\nGrafo de Localidades e Rotas:")
        for node in self.nodes.values():
            print(node)
        for route in self.edges.values():
            print(f"Rota de {route.origin} para {route.destination}, Distância: {route.distance} km, Pavimento: {route.type_pavement}, Bloqueada: {route.blocked}")
