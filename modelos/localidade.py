class Localidade:
    def __init__(self, nome, populacao, urgencia, acessibilidade, reabastecimento=False):

        if not (1 <= urgencia <= 10):
            raise ValueError("A urgência deve ser um valor entre 1 e 10.")


        self.nome = nome  
        self.populacao = populacao  
        self.urgencia = urgencia  
        self.acessibilidade = acessibilidade  
        self.reabastecimento = reabastecimento  
        self.mantimentos = 0  

    def add_mantimento(self, quantidade):

        self.mantimentos += quantidade

    def __repr__(self):

        mantimentos_str = ", ".join(str(mantimento) for mantimento in self.mantimentos)
        return (
            f"Localidade {self.nome}, População: {self.populacao}, "
            f"Urgência: {self.urgencia}, Acessibilidade: {self.acessibilidade}, "
            f"Necessidades: [{mantimentos_str}]"
        )
