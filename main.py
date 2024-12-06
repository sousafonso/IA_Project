### `main.py` - Main Execution File

import random
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
    print("\nEscolha uma opção:")
    print("1. Visualizar grafo")
    print("2. Executar algoritmo de procura")
    choice = int(input("Escolha o número correspondente à opção: "))
    return choice

def display_graph(graph):
    print("\nGrafo de Localidades e Rotas:")
    for node in graph.nodes.values():
        print(node)
    for route in graph.edges.values():
        print(f"Rota de {route.origin} para {route.destination}, Distância: {route.distance} km, Pavimento: {route.type_pavement}, Bloqueada: {route.blocked}")

def unblock_routes(graph):
    """
    Tenta desbloquear rotas bloqueadas para garantir que pelo menos uma solução seja encontrada.
    """
    for route in graph.edges.values():
        if route.blocked:
            route.blocked = False
            print(f"Rota de {route.origin} para {route.destination} foi desbloqueada.")

def deliver_supplies(graph, algorithm, transport):
    for locality in sorted(graph.nodes.values(), key=lambda loc: loc.urgency, reverse=True):
        for supply in locality.supplies:
            print(f"\nEntregando {supply} para {locality.id} (Urgência: {locality.urgency})")
            start = graph.get_node("A")  # Supondo que "A" é o ponto de partida
            goal = locality
            transport.refuel()
            path = algorithm(graph, start, goal, transport)
            if path:
                print(f"Caminho encontrado: {' -> '.join(path)}")
            else:
                print(f"Não foi possível encontrar um caminho para {locality.id}. Tentando desbloquear rotas...")
                unblock_routes(graph)
                path = algorithm(graph, start, goal, transport)
                if path:
                    print(f"Caminho encontrado após desbloquear rotas: {' -> '.join(path)}")
                else:
                    print(f"Não foi possível encontrar um caminho para {locality.id} mesmo após desbloquear rotas.")
            update_conditions(graph)

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

    while True:
        choice = display_menu()
        
        if choice == 1:
            display_graph(graph)
        
        elif choice == 2:
            algorithm_choice = int(input("Escolha o algoritmo (1: BFS, 2: DFS, 3: A*, 4: Greedy): "))
            transport_choice = int(input("Escolha o transporte (1: Camião, 2: Drone, 3: Helicóptero): "))
            transport = [truck, drone, helicopter][transport_choice - 1]
            algorithms = [bfs, dfs, a_star, greedy_search]
            algorithm = algorithms[algorithm_choice - 1]
            deliver_supplies(graph, algorithm, transport)

        continue_choice = input("\nDeseja executar outra operação? (s/n): ").lower()
        if continue_choice != 's':
            break

if __name__ == "__main__":
    main()
