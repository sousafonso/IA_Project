class Localidade:
    def __init__(self, nome, populacao, urgencia, acessibilidade, reabastecimento=False):

        self.nome = nome  # Identificador da localidade
        self.populacao = populacao  # População residente
        self.urgencia = urgencia  # Urgência da localidade
        self.acessibilidade = acessibilidade  # Tipo de pavimento, não sei até que ponto é preciso este
        self.reabastecimento = reabastecimento  # Indica se é ponto de reabastecimento
        self.mantimentos = []  # Lista de mantimentos necessários para esta localidade

    def add_mantimento(self, nome, quantidade):

        self.mantimentos.append({"nome": nome, "quantidade": quantidade})

    def __repr__(self):

        mantimentos_str = ", ".join(str(mantimento) for mantimento in self.mantimentos)
        return (
            f"Localidade {self.nome}, População: {self.populacao}, "
            f"Urgência: {self.urgencia}, Acessibilidade: {self.acessibilidade}, "
            f"Necessidades: [{mantimentos_str}]"
        )
