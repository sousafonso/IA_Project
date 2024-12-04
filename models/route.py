class Route:
    PAVEMENT_MULTIPLIER = {
        "asfalto": 1.0,
        "trilha": 2.0,
        "terra": 1.5,
    }

    def __init__(self, route_id, origin, destination, distance, type_pavement, restrictions = None):
        """
        :param route_id: identificador da rota
        
        
        """
        self.route_id = route_id
        self.origin = origin
        self.destination = destination
        self.distance = distance
        self.type_pavement = type_pavement
        self.restrictions = restrictions if restrictions else []
        self.blocked = False

        def update_blockage (self, blockage):
            if (blockage) in ["deslizamento", "acidente", "pista molhada", "neve"]:
                self.blockage = True

        def is_accessible_by_transport(self, transport_type):
            if self.blocked:
                return False
            return transport_type in self.restrictions
        
        def get_cost(self):
            multiplier = self.PAVEMENT_MULTIPLIER.get(self.type_pavement, 1.0)
            return self.distance * multiplier
        
        def calculate_time(self, speed):
            return self.distance / speed