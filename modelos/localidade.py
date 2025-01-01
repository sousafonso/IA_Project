class Localidade:
    def __init__(self, nome, populacao, urgencia, acessibilidade):

        self.nome = nome  # Identificador da localidade
        self.populacao = populacao  # População residente
        self.urgencia = urgencia  # Urgência da localidade
        self.acessibilidade = acessibilidade  # Tipo de pavimento, não sei até que ponto é preciso este
        self.mantimentos = []  # Lista de mantimentos necessários para esta localidade

    def add_mantimento(self, mantimento):
        """
        Adiciona mantimentos à lista de necessidades da localidade.
        
        :param mantimento: Objeto da classe mantimento representando o mantimento.
        """
        self.mantimentos.append(mantimento)

    def __repr__(self):
        """
        Representação da localidade para exibição no terminal.
        """
        mantimentos_str = ", ".join(str(mantimento) for mantimento in self.mantimentos)
        return (
            f"Localidade {self.nome}, População: {self.populacao}, "
            f"Urgência: {self.urgencia}, Acessibilidade: {self.acessibilidade}, "
            f"Necessidades: [{mantimentos_str}]"
        )
