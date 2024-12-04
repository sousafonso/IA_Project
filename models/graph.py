class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, locality):
        self.nodes[locality.id] = locality

    def add_edge(self, route, origin, destination):
        self.edges[(origin.id, destination.id)] = route

    def get_node(self, id):
        return self.nodes[id]
    
    def get_neighbours(self, node):
        neighbours = []
        for (origin, destination) in self.edges.items():
            if origin == node.id and not destination.blocked:
                neighbours.append(destination)
        return neighbours
    
    def get_neighbours_with_routes (self, node):
        neighbours = []
        for (origin, destination) in self.edges.items():
            if origin == node.id and not route.blocked:
                neighbours.append((destination, route))
        return neighbours
    
    def cost(self, origin, destination):
        return self.edges[(origin, destination)].get_cost()

    def neighbors(self, node):
        neighbors = []
        for (origin_id, destination_id), route in self.edges.items():
            if origin_id == node and not route.blocked:
                neighbors.append(self.nodes[destination_id])
        return neighbors