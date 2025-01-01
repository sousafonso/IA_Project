from modelos.localidade import Localidade
from modelos.rota import Rota
from modelos.grafo import Grafo

# Criar localidades
loc_a = Localidade("Guimarães", population=500, urgency=3, accessibility="asfalto")
loc_b = Localidade("Braga", population=300, urgency=5, accessibility="terra")
loc_c = Localidade("Fafe", population=800, urgency=2, accessibility="trilha")
loc_d = Localidade("Vizela", population=1000, urgency=1, accessibility="asfalto")
loc_e = Localidade("Ponte de Lima", population=200, urgency=4, accessibility="terra")

# Criar o grafo
graph = Grafo()

# Adicionar localidades ao grafo
for loc in [loc_a, loc_b, loc_c, loc_d, loc_e]:
    graph.add_node(loc)

# Adicionar rotas entre localidades
graph.add_edge("Guimarães", "Braga", 50, "asfalto", restrictions=["camião", "drone"])
graph.add_edge("Guimarães", "Fafe", 70, "terra", restrictions=["drone"])
graph.add_edge("Braga", "Vizela", 40, "trilha", restrictions=["helicóptero"])
graph.add_edge("Fafe", "Ponte de Lima", 60, "terra", restrictions=["camião"])
graph.add_edge("Vizela", "Ponte de Lima", 80, "asfalto", restrictions=[])

# Visualizar o grafo (em formato textual)
graph.display()
