class Rota:
    PAVEMENT_MULTIPLIER = {
        "asfalto": 1.0,
        "terra": 1.5,
        "trilha": 2.0,
    }

    def __init__(self, numero, origem, destino, distancia, pavimento, restricoes=None):
        """
        :restrições: Lista de tipos de transporte que não podem acessar esta rota.
        """
        self.numero = numero  # Identificador da rota
        self.origem = origem  # Localidade de origem
        self.destino = destino  # Localidade de destino
        self.distancia = distancia  # Distância entre as localidades
        self.pavimento = pavimento  # Tipo de pavimento
        self.restricoes = restricoes if restricoes else []  # Restrições de acesso
        self.bloqueado = False  # Indica se a rota está bloqueada

    def update_blockage(self, blockage):
        """
        Atualiza o estado de bloqueio da rota com base em uma condição.
        
        :param blockage: Razão para o bloqueio (e.g., 'deslizamento', 'neve').
        """
        if blockage in ["deslizamento", "neve", "acidente"]:
            self.bloqueado = True
        else:
            self.bloqueado = False

    def is_accessible_by_transport(self, transport_type):
        """
        Verifica se a rota está acessível para um tipo de transporte.
        
        :param transport_type: Tipo de transporte (e.g., 'camião', 'drone').
        :return: True se a rota estiver acessível, False caso contrário.
        """
        if self.bloqueado:
            return False
        return transport_type not in self.restricoes

    def get_cost(self):
        """
        Calcula o custo da rota com base na distância e no tipo de pavimento.
        
        :return: O custo total da rota.
        """
        multiplier = self.PAVEMENT_MULTIPLIER.get(self.pavimento, 1.0)
        return self.distancia * multiplier

    def calculate_time(self, speed):
        """
        Calcula o tempo necessário para percorrer a rota.
        
        :param speed: Velocidade do transporte (em km/h).
        :return: Tempo necessário (em horas).
        """
        return self.distancia / speed if speed > 0 else float('inf')

    def __repr__(self):
        """
        Representação textual da rota para exibição no terminal.
        """
        return (
            f"Rota {self.route_id}: {self.origem} -> {self.destino}, "
            f"Distância: {self.distancia} km, Pavimento: {self.pavimento}, "
            f"Restrições: {self.restricoes}, Bloqueada: {self.bloqueado}"
        )
