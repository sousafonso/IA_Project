import random
import networkx as nx
import matplotlib.pyplot as plt
from models.locality import Locality
from models.transport import Transport
from models.route import Route
from models.graph import Graph
from models.supply import Supply
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.a_star import a_star
from algorithms.greedy_search import greedy_search

def update_conditions(graph):
    """
    Atualiza as condições de adversidade aleatoriamente, alterando a acessibilidade das rotas
    e condições das localidades após cada visita.
    """
    # Simular adversidades: bloquear rotas ou alterar o pavimento
    routes = list(graph.edges.values())
    for route in routes:
        if random.choice([True, False]):
            route.blocked = True
            print(f"Rota de {route.origin} para {route.destination} agora está bloqueada.")
        elif random.choice([True, False]):
            # Alterar pavimento
            new_pavement = random.choice(["asfalto", "terra", "trilha"])
            route.type_pavement = new_pavement
            print(f"Pavimento de {route.origin} para {route.destination} alterado para {new_pavement}.")

    # Simular mudanças nas localidades
    localities = graph.nodes.values()
    for locality in localities:
        if random.choice([True, False]):
            new_urgency = random.randint(1, 5)
            locality.urgency = new_urgency
            print(f"Urgência da localidade {locality.id} alterada para {new_urgency}.")

def run_algorithm(graph, start, goal, algorithm_choice, transport):
    """
    Executa o algoritmo escolhido para resolver o problema de procura.
    """
    heuristic = lambda x, y: 0  # Placeholder para a heurística (pode ser melhorada)

    if algorithm_choice == 1:  # BFS
        path = bfs(graph, start, goal, transport)
    elif algorithm_choice == 2:  # DFS
        path = dfs(graph, start, goal, transport)
    elif algorithm_choice == 3:  # A*
        path = a_star(graph, start, goal, transport)
    elif algorithm_choice == 4:  # Greedy
        path = greedy_search(graph, start, goal, transport)
    else:
        print("Algoritmo inválido.")
        return None

    return path

def display_graph(graph):
    """
    Exibe o grafo utilizando a biblioteca networkx e matplotlib.
    """
    G = nx.Graph()

    # Adicionar nós
    for node in graph.nodes.values():
        G.add_node(node.id, label=f"{node.id}\nUrgência: {node.urgency}")

    # Adicionar arestas
    for route in graph.edges.values():
        G.add_edge(route.origin, route.destination, label=f"{route.distance} km\n{route.type_pavement}")

    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)
    plt.show()

def display_menu():
    print("\nEscolha uma opção:")
    print("1. Executar algoritmo de procura")
    print("2. Visualizar grafo")
    choice = int(input("Escolha o número correspondente à opção: "))
    return choice

def main():
    # Criar localidades
    loc1 = Locality("A", population=500, urgency=3, accessibility="asfalto")
    loc2 = Locality("B", population=300, urgency=5, accessibility="terra")
    loc3 = Locality("C", population=800, urgency=2, accessibility="trilha")
    loc4 = Locality("D", population=1000, urgency=1, accessibility="asfalto")
    loc5 = Locality("E", population=200, urgency=4, accessibility="terra")
    loc6 = Locality("F", population=400, urgency=3, accessibility="trilha")

    # Criar mantimentos
    loc1.add_supply(Supply("água", 200))
    loc1.add_supply(Supply("medicamentos", 100))
    loc2.add_supply(Supply("água", 150))
    loc2.add_supply(Supply("roupa", 50))
    loc3.add_supply(Supply("medicamentos", 200))
    loc3.add_supply(Supply("água", 120))
    loc4.add_supply(Supply("roupa", 100))
    loc4.add_supply(Supply("medicamentos", 50))
    loc5.add_supply(Supply("água", 250))
    loc5.add_supply(Supply("roupa", 70))
    loc6.add_supply(Supply("medicamentos", 150))
    loc6.add_supply(Supply("água", 180))

    # Criar grafo
    graph = Graph()
    for loc in [loc1, loc2, loc3, loc4, loc5, loc6]:
        graph.add_node(loc)

    # Criar rotas
    graph.add_edge(Route("A", "B", distance=50, type_pavement="asfalto", restrictions=["camião", "drone"]))
    graph.add_edge(Route("A", "C", distance=70, type_pavement="terra", restrictions=["camião", "helicóptero"]))
    graph.add_edge(Route("B", "D", distance=40, type_pavement="trilha", restrictions=["helicóptero"]))
    graph.add_edge(Route("C", "E", distance=60, type_pavement="terra", restrictions=["camião"]))
    graph.add_edge(Route("D", "F", distance=30, type_pavement="asfalto", restrictions=["drone", "camião"]))
    graph.add_edge(Route("E", "F", distance=80, type_pavement="trilha", restrictions=["helicóptero"]))

    # Criar transportes
    truck = Transport(type="camião", capacity=2000, fuel_range=300, speed=80)
    drone = Transport(type="drone", capacity=500, fuel_range=100, speed=100)
    helicopter = Transport(type="helicóptero", capacity=1000, fuel_range=500, speed=150)

    # Menu interativo
    while True:
        # Exibir o menu
        choice = display_menu()

        if choice == 1:
            start = input("Digite a localidade de partida: ")
            goal = input("Digite a localidade de destino: ")
            algorithm_choice = int(input("Escolha o algoritmo (1: BFS, 2: DFS, 3: A*, 4: Greedy): "))
            transport_choice = int(input("Escolha o transporte (1: Camião, 2: Drone, 3: Helicóptero): "))
            transport = [truck, drone, helicopter][transport_choice - 1]

            # Executar o algoritmo escolhido
            print(f"\nExecutando o algoritmo {['BFS', 'DFS', 'A*', 'Greedy'][algorithm_choice - 1]}...")
            path = run_algorithm(graph, start, goal, algorithm_choice, transport)
            if path:
                print(f"Caminho encontrado: {' -> '.join(path)}")

            # Atualizar condições devido ao progresso da simulação
            update_conditions(graph)

        elif choice == 2:
            display_graph(graph)

        # Perguntar se o utilizador deseja continuar
        continue_choice = input("\nDeseja executar outra operação? (s/n): ").lower()
        if continue_choice != 's':
            break

if __name__ == "__main__":
    main()
