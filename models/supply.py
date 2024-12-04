class Supply:
    def __init__(self, type, quantity):
        """
        :param type: Tipo de mantimento (e.g., 'água', 'medicamentos', 'roupa').
        :param quantity: Quantidade necessária.
        """
        self.type = type
        self.quantity = quantity

    def __repr__(self):
        return f"{self.quantity} unidades de {self.type}"
