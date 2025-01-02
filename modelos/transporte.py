class Transporte:
    def __init__(self, tipo, capacidade, velocidade, autonomia):
        """
        Classe que representa um veículo de transporte.

        :param tipo: Tipo do transporte (e.g., 'helicóptero', 'camião', 'drone').
        :param capacidade: Capacidade máxima de carga (em unidades).
        :param velocidade: Velocidade do transporte (km/h).
        :param autonomia: Autonomia máxima do combustível (em km).
        """
        self.tipo = tipo  # Tipo do transporte
        self.capacidade = capacidade  # Capacidade máxima de carga
        self.velocidade = velocidade  # Velocidade em km/h
        self.autonomia = autonomia  # Autonomia máxima em km
        self.current_fuel = autonomia  # Quantidade atual de combustível

    def calculate_cost(self, distancia, conditions="normal"):
        """
        Calcula o custo de combustível com base na distância e nas condições da rota.

        :param distancia: Distância a ser percorrida (em km).
        :param conditions: Condições da rota ('normal' ou 'difícil').
        :return: Custo estimado (em unidades de combustível).
        """
        base_cost = distancia / self.autonomia
        if conditions == "difícil":
            base_cost *= 1.5  # Penalidade para condições difíceis
        return base_cost


    def can_access_route(self, route):
        """
        Verifica se o transporte pode acessar a rota com base nas restrições da rota.
        :param route: Objeto da classe Rota.
        :return: True se o transporte puder acessar a rota, False caso contrário.
        """
        if route.bloqueado and self.tipo in route.restricoes:
            return False  # Transporte está restrito nesta rota
        return True


    def can_complete_route(self, distancia):
        """
        Verifica se o transporte possui combustível suficiente para completar a rota.

        :param distancia: Distância a ser percorrida (em km).
        :return: True se tiver combustível suficiente, False caso contrário.
        """
        return self.current_fuel >= distancia

    def update_fuel(self, distancia):
        """
        Atualiza a quantidade de combustível após percorrer uma distância.

        :param distancia: Distância percorrida (em km).
        """
        if self.current_fuel >= distancia:
            self.current_fuel -= distancia
        else:
            raise ValueError(f"O transporte {self.tipo} não tem combustível suficiente para percorrer {distancia} km.")

    def refuel(self):
        """
        Reabastece o transporte ao seu alcance total de combustível.
        """
        self.current_fuel = self.autonomia

    def __repr__(self):
        """
        Representação textual do transporte para exibição no terminal.
        """
        return (
            f"Transporte {self.tipo}: Capacidade: {self.capacidade} unidades, "
            f"Velocidade: {self.velocidade} km/h, Autonomia: {self.autonomia} km, "
            f"Combustível atual: {self.current_fuel} km"
        )
