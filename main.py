### `main.py` - Main Execution File

import random
#import networkx as nx
#import matplotlib.pyplot as plt
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
    routes = list(graph.edges.values())
    for route in routes:
        if random.choice([True, False]):
            route.blocked = True
            print(f"Rota de {route.origin} para {route.destination} agora está bloqueada.")
        elif random.choice([True, False]):
            new_pavement = random.choice(["asfalto", "terra", "trilha"])
            route.type_pavement = new_pavement
            print(f"Pavimento de {route.origin} para {route.destination} alterado para {new_pavement}.")

def display_menu():
    while True:
        try:
            print("\nEscolha uma opção:")
            print("1. Visualizar grafo")
            print("2. Executar algoritmo de procura")
            choice = int(input("Escolha o número correspondente à opção: "))
            if choice in [1, 2]:
                return choice
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")
'''
def display_graph(graph):
    G = nx.DiGraph()
    for node in graph.nodes.values():
        G.add_node(node.id, label=f"{node.id}\nUrgência: {node.urgency}")
    for route in graph.edges.values():
        G.add_edge(route.origin, route.destination, label=f"{route.distance} km\n{route.type_pavement}", color='red' if route.blocked else 'black')

    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'label')
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]

    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', edge_color=edge_colors)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='green')
    plt.show()
'''
def unblock_routes(graph):
    """
    Tenta desbloquear rotas bloqueadas para garantir que pelo menos uma solução seja encontrada.
    """
    for route in graph.edges.values():
        if route.blocked:
            route.blocked = False
            print(f"Rota de {route.origin} para {route.destination} foi desbloqueada.")

def deliver_supplies(graph, algorithm, transport):
    all_paths = []
    for locality in sorted(graph.nodes.values(), key=lambda loc: loc.urgency, reverse=True):
        for supply in locality.supplies:
            print(f"\nEntregando {supply} para {locality.id} (Urgência: {locality.urgency})")
            start = graph.get_node("A")  # Supondo que "A" é o ponto de partida
            goal = locality
            transport.refuel()
            path = algorithm(graph, start, goal, transport)
            if path:
                print(f"Caminho encontrado: {' -> '.join(path)}")
                all_paths.append(path)
            else:
                print(f"Não foi possível encontrar um caminho para {locality.id}. Tentando desbloquear rotas...")
                unblock_routes(graph)
                path = algorithm(graph, start, goal, transport)
                if path:
                    print(f"Caminho encontrado após desbloquear rotas: {' -> '.join(path)}")
                    all_paths.append(path)
                else:
                    print(f"Não foi possível encontrar um caminho para {locality.id} mesmo após desbloquear rotas.")
            update_conditions(graph)
    print("\nCaminhos realizados para entregar todos os mantimentos:")
    for path in all_paths:
        print(" -> ".join(path))

def main():
    loc1 = Locality("A", population=500, urgency=3, accessibility="asfalto")
    loc2 = Locality("B", population=300, urgency=5, accessibility="terra")
    loc3 = Locality("C", population=800, urgency=2, accessibility="trilha")
    loc4 = Locality("D", population=1000, urgency=1, accessibility="asfalto")
    loc5 = Locality("E", population=200, urgency=4, accessibility="terra")
    loc6 = Locality("F", population=400, urgency=3, accessibility="trilha")

    graph = Graph()
    for loc in [loc1, loc2, loc3, loc4, loc5, loc6]:
        graph.add_node(loc)

    graph.add_edge("A", "B", 50, "asfalto", restrictions=["camião", "drone"])
    graph.add_edge("A", "C", 70, "terra", restrictions=["camião", "helicóptero"])
    graph.add_edge("B", "D", 40, "trilha", restrictions=["helicóptero"])
    graph.add_edge("C", "E", 60, "terra", restrictions=["camião"])
    graph.add_edge("D", "F", 30, "asfalto", restrictions=["drone", "camião"])
    graph.add_edge("E", "F", 80, "trilha", restrictions=["helicóptero"])

    truck = Transport(type="camião", capacity=2000, fuel_range=300, speed=80)
    drone = Transport(type="drone", capacity=500, fuel_range=100, speed=100)
    helicopter = Transport(type="helicóptero", capacity=1000, fuel_range=500, speed=150)

    choice = display_menu()
    
    if choice == 1:
        display_graph(graph)
    
    elif choice == 2:
        while True:
            try:
                algorithm_choice = int(input("Escolha o algoritmo (1: BFS, 2: DFS, 3: A*, 4: Greedy): "))
                if algorithm_choice in [1, 2, 3, 4]:
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")
        
        while True:
            try:
                transport_choice = int(input("Escolha o transporte (1: Camião, 2: Drone, 3: Helicóptero): "))
                if transport_choice in [1, 2, 3]:
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")
        
        transport = [truck, drone, helicopter][transport_choice - 1]
        algorithms = [bfs, dfs, a_star, greedy_search]
        algorithm = algorithms[algorithm_choice - 1]
        deliver_supplies(graph, algorithm, transport)

if __name__ == "__main__":
    main()
