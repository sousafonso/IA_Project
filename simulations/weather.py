#Desenvolver um sistema que utilize algoritmos de procura para otimizar a distribuição de suprimentos 
# (alimentos, água, medicamentos) em zonas afetadas por uma catástrofe natural. O sistema deve garantir a 
# eficiência no uso dos recursos e priorizar as áreas mais necessitadas, maximizando a assistência no menor tempo possível.

# Implementa a simulação de condições meteorológicas, afetando as rotas e as zonas com eventos como tempestades que alteram a acessibilidade e a velocidade dos veículos.

class Weather:

    def __init__(self, severity, duration):
        self.severity = severity
        self.duration = duration

    def update(self):
        self.duration -= 1
        if self.duration == 0:
            self.severity = 0
        return self.severity

    def is_severe(self):
        return self.severity > 0

    def is_clear(self):
        return self.severity == 0
    
    