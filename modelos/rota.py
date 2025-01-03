class Rota:
    def __init__(self, numero, origem, destino, distancia, pavimento, restricoes=None):
        """
        :restrições: Lista de tipos de transporte que não podem acessar esta rota.
        """
        self.numero = numero  
        self.origem = origem  
        self.destino = destino  
        self.distancia = distancia  
        self.temp_cost = distancia
        self.pavimento = pavimento  
        self.restricoes = restricoes if restricoes else []  
        self.bloqueado = False  


    def update_blockage(self, blockage):
        """
        Atualiza o estado de bloqueio da rota com base em um evento.
        :param blockage: Tipo de bloqueio (e.g., 'tempestade', 'estrada bloqueada').
        """
        self.bloqueado = True
        self.restricoes.append(blockage)
        if blockage == "tempestade":
            self.restricoes.extend(["drone","helicóptero"]) 
        elif blockage == "estrada bloqueada":
            self.restricoes.append("camião")  


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

        return self.distancia

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
