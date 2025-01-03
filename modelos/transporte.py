class Transporte:
    def __init__(self, tipo, capacidade, velocidade, autonomia):
        self.tipo = tipo  # Tipo do transporte
        self.capacidade = capacidade  # Capacidade máxima de carga
        self.velocidade = velocidade  # Velocidade em km/h
        self.autonomia = autonomia  # Autonomia máxima em km
        self.current_fuel = autonomia  # Quantidade atual de combustível
        self.carga_atual = 0

    def getVelocidade(self):
        return self.velocidade

    def carregar(self, carga):
        if self.carga_atual + carga > self.capacidade:
            raise ValueError("Capacidade máxima excedida!")
        self.carga_atual += carga

    def descarregar(self, carga):
        if self.carga_atual - carga < 0:
            raise ValueError("Carga insuficiente para descarregar!")
        self.carga_atual -= carga

    def calcular_reabastecimento(self, grafo, local_atual):
        pontos_reabastecimento = [
            local for local in grafo.nodes.values() if local.reabastecimento
        ]
        menor_distancia = float("inf")
        proximo_reabastecimento = None

        for ponto in pontos_reabastecimento:
            rota = grafo.get_route(local_atual, ponto)
            if rota and rota.distancia < menor_distancia:
                menor_distancia = rota.distancia
                proximo_reabastecimento = ponto

        return proximo_reabastecimento


    def calculate_cost(self, distancia, conditions="normal"):

        base_cost = distancia / self.autonomia
        if conditions == "difícil":
            base_cost *= 1.5  # Penalidade para condições difíceis
        return base_cost


    def can_access_route(self, route):

        if route.bloqueado and self.tipo in route.restricoes:
            return False  # Transporte está restrito nesta rota
        return True


    def can_complete_route(self, distancia):

        return self.current_fuel >= distancia

    def update_fuel(self, distancia):

        if self.current_fuel >= distancia:
            self.current_fuel -= distancia
        else:
            raise ValueError(f"O transporte {self.tipo} não tem combustível suficiente para percorrer {distancia} km.")

    def refuel(self):

        self.current_fuel = self.autonomia

    def __repr__(self):

        return (
            f"Transporte {self.tipo}: Capacidade: {self.capacidade} unidades, "
            f"Velocidade: {self.velocidade} km/h, Autonomia: {self.autonomia} km, "
            f"Combustível atual: {self.current_fuel} km"
        )
