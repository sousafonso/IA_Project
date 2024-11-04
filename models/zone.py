#Desenvolver um sistema que utilize algoritmos de procura para otimizar a distribuição de suprimentos 
# (alimentos, água, medicamentos) em zonas afetadas por uma catástrofe natural. O sistema deve garantir a 
# eficiência no uso dos recursos e priorizar as áreas mais necessitadas, maximizando a assistência no menor tempo possível.

# Define a classe Zone, que representa uma zona de entrega, contendo atributos como população, nível de gravidade e restrições de acesso.

def __init__(self, id, population, severity, coordinates, access_restrictions) :
    self.id = id
    self.population = population
    self.severity = severity
    self.coordinates = coordinates
    self.access_restrictions = access_restrictions

def update_conditions(self, weather) :
    self.severity = weather.severity

def is_accessible(self, vehicle) :
    return vehicle.access_level >= self.access_restrictions

