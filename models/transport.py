class Transport:
    def __init__(self, type, capacity, speed, fuel_range): # capacity é a capacidade de carga, speed é a velocidade e fuel_range é a autonomia em km 
        """
        :param type: tipo de transporte (camião, drone, helicóptero)
        :param capacity: capacidade máxima de carga
        :param speed: velocidade do veiculo em km/h
        :param fuel_range: autonomia do veiculo em km
        """
        self.type = type
        self.capacity = capacity
        self.speed = speed
        self.fuel_range = fuel_range

    def calculate_cost(self, distance, conditions):
        base_cost = distance / self.fuel_range
        if conditions == "difícil":
            return base_cost * 1.5

    def can_access_route(self, route):
        return route.is_accessible_by_transport(self.type)