class Route:
    PAVEMENT_MULTIPLIER = {
        "asfalto": 1.0,
        "trilha": 2.0,
        "terra": 1.5,
    }

    def __init__(self, route_id, origin, destination, distance, type_pavement, restrictions=None):
        """
        :param route_id: identificador da rota
        :param origin: localidade de origem
        :param destination: localidade de destino
        :param distance: distância entre as localidades
        :param type_pavement: tipo de pavimento da rota
        :param restrictions: lista de restrições de acesso à rota
        """
        self.route_id = route_id
        self.origin = origin
        self.destination = destination
        self.distance = distance
        self.type_pavement = type_pavement
        self.restrictions = restrictions if restrictions else []
        self.blocked = False

    def update_blockage(self, blockage):
        """
        Atualiza o estado de bloqueio da rota com base em uma condição.
        :param blockage: Condição que pode bloquear a rota (e.g., 'deslizamento', 'neve').
        """
        if blockage in ["deslizamento", "acidente", "pista molhada", "neve"]:
            self.blocked = True

    def is_accessible_by_transport(self, transport_type):
        """
        Verifica se a rota está acessível pelo tipo de transporte.
        :param transport_type: Tipo de transporte.
        :return: True se acessível, False caso contrário.
        """
        if self.blocked:
            return False
        return transport_type not in self.restrictions

    def get_cost(self):
        """
        Calcula o custo da rota com base no tipo de pavimento.
        """
        multiplier = self.PAVEMENT_MULTIPLIER.get(self.type_pavement, 1.0)
        return self.distance * multiplier

    def calculate_time(self, speed):
        """
        Calcula o tempo necessário para percorrer a rota.
        :param speed: Velocidade do transporte (km/h).
        :return: Tempo (em horas).
        """
        return self.distance / speed