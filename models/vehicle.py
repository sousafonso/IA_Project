#Desenvolver um sistema que utilize algoritmos de procura para otimizar a distribuição de suprimentos 
# (alimentos, água, medicamentos) em zonas afetadas por uma catástrofe natural. O sistema deve garantir a 
# eficiência no uso dos recursos e priorizar as áreas mais necessitadas, maximizando a assistência no menor tempo possível.

# Define a classe Vehicle, que representa os veículos de transporte, com atributos como tipo, capacidade de carga e autonomia de combustível.

def __init__(self, id, type, max_load, fuel_capacity, range):
    self.id = id
    self.type = type
    self.max_load = max_load
    self.fuel_capacity = fuel_capacity
    self.range = range
    self.current_load = 0
    self.current_fuel = fuel_capacity
    self.current_range = range
    self.current_position = None
    self.current_route = []
    self.current_plan = []

def can_access(self, zone):
    return self.current_range >= zone.distance

def update_range(self, distance):
    self.current_range -= distance