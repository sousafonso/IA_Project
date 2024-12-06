from models.route import Route

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, locality):
        """
        Adiciona uma localidade ao grafo.
        :param locality: Objeto da classe Locality.
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
        route = Route(f"{origin}-{destination}", origin, destination, distance, type_pavement, restrictions)
        self.edges[(origin, destination)] = route
        
    def get_node(self, id):
        """
        Obtém uma localidade pelo seu identificador.
        """
        return self.nodes.get(id)
    
    def get_neighbors(self, node):
        """
        Obtém os vizinhos de uma localidade.
        :param node: Localidade atual.
        :return: Lista de localidades vizinhas.
        """
        neighbors = []
        for (origin, destination), route in self.edges.items():
            if origin == node.id and not route.blocked:
                neighbors.append(self.nodes[destination])
        return neighbors

    def get_route(self, origin, destination):
        """
        Obtém a rota entre duas localidades.
        """
        return self.edges.get((origin.id, destination.id))
    
    def cost(self, origin, destination):
        """
        Obtém o custo da rota entre duas localidades.
        """
        route = self.get_route(origin, destination)
        if route:
            return route.get_cost()
        return float('inf')