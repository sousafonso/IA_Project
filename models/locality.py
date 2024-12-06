class Locality:
    def __init__(self, id, population, urgency, accessibility):
        """
        :param id: Identificador da localidade.
        :param population: População da localidade.
        :param urgency: Nível de urgência da localidade.
        :param accessibility: Tipo de pavimento ou condição de acesso (e.g., 'asfalto', 'terra').
        """
        self.id = id
        self.population = population
        self.urgency = urgency
        self.accessibility = accessibility
        self.supplies = []  # Lista de mantimentos necessários

    def add_supply(self, supply):
        """
        Adiciona mantimentos à lista de necessidades da localidade.
        :param supply: Objeto da classe Supply.
        """
        self.supplies.append(supply)

    def __repr__(self):
        supplies_str = ", ".join(str(supply) for supply in self.supplies)
        return f"Localidade {self.id}, Urgência: {self.urgency}, Necessidades: [{supplies_str}]"