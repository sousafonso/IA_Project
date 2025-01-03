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

        return self.nodes.get(nome)

    def get_route(self, origem, destino):

        return self.edges.get((origem.nome, destino.nome))


    def get_neighbors(self, node):

        neighbors = []
        for (origin, destination), route in self.edges.items():
            if origin == node.nome and not route.bloqueado:  
                neighbors.append(self.nodes[destination])
        return neighbors

    def update_costs_for_vehicle(self, vehicle_speed):

        for route in self.edges.values():
            route.temp_cost = route.calculate_time(vehicle_speed)  

    def restore_original_costs(self):

        for route in self.edges.values():
            route.temp_cost = route.distancia



    def display(self):
        print("\nGrafo de Localidades e Rotas:")
        for node in self.nodes.values():
            print(node)
        for route in self.edges.values():
            print(f"Rota de {route.origem} para {route.destino}, Distância: {route.distancia} km, Pavimento: {route.pavimento}, Bloqueada: {route.bloqueado}")
