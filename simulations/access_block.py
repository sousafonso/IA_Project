# Desenvolver um sistema que utilize algoritmos de procura para otimizar a distribuição de suprimentos 
# (alimentos, água, medicamentos) em zonas afetadas por uma catástrofe natural. O sistema deve garantir a 
# eficiência no uso dos recursos e priorizar as áreas mais necessitadas, maximizando a assistência no menor tempo possível.

# Modela e simula bloqueios de acesso em certas rotas, como estradas destruídas, e controla o tempo que essas rotas permanecem bloqueadas.

class AccessBlock:
        
        def __init__(self, route, duration):
            self.route = route
            self.duration = duration
    
        def update(self):
            self.duration -= 1
            return self.duration
    
        def is_active(self):
            return self.duration > 0
        
        def is_route_blocked(self, zone1, zone2):
            return (zone1, zone2) in self.route or (zone2, zone1) in self.route
