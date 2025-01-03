class Rota:
    def __init__(self, numero, origem, destino, distancia, pavimento, restricoes=None):

        self.numero = numero  
        self.origem = origem  
        self.destino = destino  
        self.distancia = distancia  
        self.temp_cost = distancia
        self.pavimento = pavimento  
        self.restricoes = restricoes if restricoes else []  
        self.bloqueado = False  


    def update_blockage(self, blockage):

        self.bloqueado = True
        self.restricoes.append(blockage)
        if blockage == "tempestade":
            self.restricoes.extend(["drone","helicóptero"]) 
        elif blockage == "estrada bloqueada":
            self.restricoes.append("camião")  


    def is_accessible_by_transport(self, transport_type):

        if self.bloqueado:
            return False
        return transport_type not in self.restricoes

    def get_cost(self):

        return self.distancia

    def calculate_time(self, speed):

        return self.distancia / speed if speed > 0 else float('inf')

    def __repr__(self):

        return (
            f"Rota {self.route_id}: {self.origem} -> {self.destino}, "
            f"Distância: {self.distancia} km, Pavimento: {self.pavimento}, "
            f"Restrições: {self.restricoes}, Bloqueada: {self.bloqueado}"
        )
