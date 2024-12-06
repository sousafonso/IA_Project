class Transport:
    def __init__(self, type, capacity, speed, fuel_range):
        """
        :param type: Tipo do transporte (e.g., 'helicóptero', 'camião', 'drone').
        :param capacity: Capacidade máxima de carga.
        :param speed: Velocidade do transporte (km/h).
        :param fuel_range: Autonomia de combustível (km).
        """
        self.type = type
        self.capacity = capacity
        self.speed = speed
        self.fuel_range = fuel_range
        self.current_fuel = fuel_range

    def calculate_cost(self, distance, conditions):
        """
        Calcula o custo de combustível com base na distância e nas condições da rota.
        :param distance: Distância a ser percorrida.
        :param conditions: Condições da rota ('normal' ou 'difícil').
        :return: Custo estimado.
        """
        base_cost = distance / self.fuel_range
        if conditions == "difícil":
            base_cost *= 1.5
        return base_cost

    def can_access_route(self, route):
        """
        Verifica se o transporte pode acessar a rota.
        :param route: Objeto da classe Route.
        :return: True se o transporte puder acessar a rota, False caso contrário.
        """
        return self.type not in route.restrictions

    def can_complete_route(self, distance):
        """
        Verifica se o transporte possui combustível suficiente para percorrer a rota.
        :param distance: Distância a ser percorrida.
        :return: True se tiver combustível suficiente, False caso contrário.
        """
        return self.current_fuel >= distance

    def update_fuel(self, distance):
        """
        Atualiza a quantidade de combustível após percorrer uma distância.
        :param distance: Distância percorrida.
        """
        self.current_fuel -= distance

    def refuel(self):
        """
        Reabastece o transporte ao seu alcance total de combustível.
        """
        self.current_fuel = self.fuel_range