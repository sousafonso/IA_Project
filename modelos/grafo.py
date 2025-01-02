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

    def get_route(self, origem, destino):
        """
        Obtém a rota entre duas localidades.
        :param origem: Objeto da classe Localidade (origem).
        :param destino: Objeto da classe Localidade (destino).
        :return: Objeto Rota ou None se não existir.
        """
        return self.edges.get((origem.nome, destino.nome))


    def get_neighbors(self, node):
        """
        Retorna os vizinhos de um nó.
        :param node: Objeto da classe Localidade.
        :return: Lista de objetos Localidade que são vizinhos.
        """
        neighbors = []
        for (origin, destination), route in self.edges.items():
            if origin == node.nome and not route.bloqueado:  # Verifica se a rota não está bloqueada
                neighbors.append(self.nodes[destination])
        return neighbors

    def update_costs_for_vehicle(self, vehicle_speed):
        """
        Atualiza os custos das rotas no grafo para refletir o tempo de viagem baseado na velocidade do veículo.
        :param vehicle_speed: Velocidade média do veículo (km/h).
        """
        for route in self.edges.values():
            route.temp_cost = route.calculate_time(vehicle_speed)  # Calcula o tempo de viagem

    def restore_original_costs(self):
        """
        Restaura os custos originais (distâncias) das rotas.
        """
        for route in self.edges.values():
            route.temp_cost = route.distancia



    def display(self):
        print("\nGrafo de Localidades e Rotas:")
        for node in self.nodes.values():
            print(node)
        for route in self.edges.values():
            print(f"Rota de {route.origem} para {route.destino}, Distância: {route.distancia} km, Pavimento: {route.pavimento}, Bloqueada: {route.bloqueado}")
