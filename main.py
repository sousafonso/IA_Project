import os
import random
from modelos.localidade import Localidade
from modelos.rota import Rota
from modelos.grafo import Grafo
from modelos.transporte import Transporte
from algoritmos.bfs import bfs
from algoritmos.dfs import dfs
from algoritmos.a_star import a_star
from algoritmos.greedy import greedy_search
from algoritmos.custo_uniforme import uniform_cost_search
from utils.heuristica import heuristic
from utils.visualizacao import visualize_graph_with_image

def clear_screen():

    os.system('cls' if os.name == 'nt' else 'clear')

def display_main_menu(graph):

    while True:
        print("\nMenu Principal:")
        print("1. Visualizar Grafo")
        print("2. Escolher Algoritmo de Procura")
        print("0. Sair")

        try:
            option = int(input("Escolhe uma opção: "))
            if option == 1:
                visualize_graph(graph)
            elif option == 2:
                display_algorithm_menu(graph)
            elif option == 0:
                print("A sair do programa.")
                break
            else:
                print("A opção não existe. Tenta novamente.")
        except ValueError:
            print("Entrada inválida")

def visualize_graph(graph):
    clear_screen()
    print("\nGráfico:")
    visualize_graph_with_image(graph)
    input("\nPressiona Enter para voltar ao menu...")

def display_algorithm_menu(graph):

    while True:
        simulate_events(graph)
        clear_screen()

        print("\nEscolhe o algoritmo de procura:")
        print("1. BFS")
        print("2. DFS")
        print("3. A*")
        print("4. Greedy Search")
        print("5. Custo Uniforme")
        print("0. Voltar ao Menu Principal")

        try:
            option = int(input("Escolha uma opção: "))
            if option == 1:
                execute_algorithm("BFS", graph)
            elif option == 2:
                execute_algorithm("DFS", graph)
            elif option == 3:
                execute_algorithm("A*", graph)
            elif option == 4:
                execute_algorithm("Greedy Search", graph)
            elif option == 5:
                execute_algorithm("Custo Uniforme", graph)
            elif option == 0:
                print("A voltar ao menu principal.")
                break
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")

def execute_algorithm(algorithm, graph):

    clear_screen()
    print(f"A executar {algorithm}...")
    start = input("Digite a localidade inicial: ").strip()

    if not graph.get_node(start):
        print(f"A localidade '{start}' não existe no mapa.")
        input("\Pressiona Enter para voltar ao menu...")
        return
    
    simulated_changes = simulate_events(graph, reduce_probability=True)
    print("\n--- Alterações Iniciais ---")
    for change in simulated_changes:
        print(change)

    veiculos = {
        "camião": Transporte("camião", 5000, 60, 1200),
        "drone": Transporte("drone", 600, 200, 200),
        "helicóptero": Transporte("helicóptero", 2000, 150, 400),
    }

    results = []
    for vehicle, transporte in veiculos.items():
        print(f"\nA calcular o melhor percurso para o veículo: {vehicle}")
        graph_state_backup = {node.nome: node.mantimentos for node in graph.nodes.values()}  
        graph.update_costs_for_vehicle(transporte.getVelocidade())

        path = []

        if algorithm == "BFS":
            path, tempo = bfs(graph, start, transporte)
        elif algorithm == "DFS":
            path, tempo = dfs(graph, start, transporte)
        elif algorithm == "A*":
            path, tempo = a_star(graph, start, heuristic, transporte)
        elif algorithm == "Greedy Search":
            path, tempo = greedy_search(graph, start, transporte, heuristic)
        elif algorithm == "Custo Uniforme":
            path, tempo = uniform_cost_search(graph, start, transporte)
        else:
            print("Algoritmo não reconhecido.")
            return
        
        total_entregue = sum(
            graph_state_backup[nome] - graph.get_node(nome).mantimentos
            for nome in graph_state_backup.keys()
        )

        for nome, mantimentos in graph_state_backup.items():
            graph.get_node(nome).mantimentos = mantimentos

        if path:
            results.append((vehicle, path, tempo, total_entregue))
            print(f"Veículo: {vehicle.capitalize()}, Percurso: {' -> '.join(path)}, Duração: {tempo} horas, Mantimentos entregues: {total_entregue}")
        else:
            print(f"Não foi possível encontrar um percurso para o veículo: {vehicle.capitalize()}")

        graph.restore_original_costs()

    if results:
        best_vehicle = min(
            results, key=lambda x: (x[2] / x[3], x[2]) if x[3] > 0 else (float('inf'), float('inf'))
        )
        print(f"\nMelhor veículo: {best_vehicle[0].capitalize()}, Percurso: {' -> '.join(best_vehicle[1])}, Duração: {best_vehicle[2]} horas, Mantimentos entregues: {best_vehicle[3]}")
    else:
        print("\nNão foi possível encontrar um percurso para nenhum veículo.")

    input("\nPressiona Enter para voltar ao menu...")


def simulate_events(graph, reduce_probability=True):

    alterations = []

    print("\n--- Simulação de eventos ---")

    for (origem, destino), route in graph.edges.items():
        if reduce_probability:
            prob_tempestade = 0.1  
            prob_estrada = 0.15  
        else:
            prob_tempestade = 0.2
            prob_estrada = 0.3

        imprevisto = random.choice(["tempestade", "estrada bloqueada", None])  
        if imprevisto == "tempestade" and random.random() < prob_tempestade:
            route.update_blockage("tempestade")
            alterations.append(f"Rota de {origem} para {destino} foi bloqueada devido a uma tempestade.")
        elif imprevisto == "estrada bloqueada" and random.random() < prob_estrada:
            route.update_blockage("estrada bloqueada")
            alterations.append(f"Rota de {origem} para {destino} foi marcada como 'estrada bloqueada'.")

    for node in graph.nodes.values():
        if random.random() < 0.2:  
            old_urgency = node.urgencia
            new_urgency = random.randint(1, 10)
            node.urgencia = max(1, min(10, new_urgency))  
            alterations.append(f"Urgência de {node.nome} mudou de {old_urgency} para {node.urgencia}.")

    print("\n--- Fim da Simulação ---")

    return alterations



if __name__ == "__main__":
    loc_a = Localidade("Guimarães", populacao=2000, urgencia=1, acessibilidade="asfalto", reabastecimento=True)
    loc_b = Localidade("Braga", populacao=1500, urgencia=5, acessibilidade="terra")
    loc_c = Localidade("Fafe", populacao=1200, urgencia=1, acessibilidade="trilha", reabastecimento=True)
    loc_d = Localidade("Vizela", populacao=1800, urgencia=4, acessibilidade="asfalto")
    loc_e = Localidade("Ponte de Lima", populacao=900, urgencia=1, acessibilidade="terra", reabastecimento=True)
    loc_f = Localidade("Porto", populacao=1870, urgencia=2, acessibilidade="asfalto")
    loc_g = Localidade("Lisboa", populacao=2500, urgencia=6, acessibilidade="paralelo")
    loc_h = Localidade("Coimbra", populacao=3780, urgencia=1, acessibilidade="terra", reabastecimento=True)
    loc_i = Localidade("Aveiro", populacao=10000, urgencia=5, acessibilidade="asfalto")
    loc_j = Localidade("Évora", populacao=1870, urgencia=1, acessibilidade="terra", reabastecimento=True)
    loc_k = Localidade("Faro", populacao=2000, urgencia=8, acessibilidade="asfalto")

    loc_a.add_mantimento(0)
    loc_b.add_mantimento(700)
    loc_c.add_mantimento(0)
    loc_d.add_mantimento(360)
    loc_e.add_mantimento(0)
    loc_f.add_mantimento(900)
    loc_g.add_mantimento(650)
    loc_h.add_mantimento(0)
    loc_i.add_mantimento(4570)
    loc_j.add_mantimento(0)
    loc_k.add_mantimento(630)

    graph = Grafo()

    for loc in [loc_a, loc_b, loc_c, loc_d, loc_e, loc_f, loc_g, loc_h, loc_i, loc_j, loc_k]:
        graph.add_node(loc)

    graph.add_edge("Guimarães", "Braga", 50, "asfalto", restricoes=["camião", "drone"])
    graph.add_edge("Braga", "Guimarães", 50, "asfalto", restricoes=["camião", "drone"])
    graph.add_edge("Guimarães", "Fafe", 70, "terra", restricoes=["drone"])
    graph.add_edge("Fafe", "Guimarães", 70, "terra", restricoes=["drone"])
    graph.add_edge("Braga", "Vizela", 40, "trilha", restricoes=["helicóptero"])
    graph.add_edge("Vizela", "Braga", 40, "trilha", restricoes=["helicóptero"])
    graph.add_edge("Fafe", "Ponte de Lima", 60, "terra", restricoes=["camião"])
    graph.add_edge("Ponte de Lima", "Fafe", 60, "terra", restricoes=["camião"])
    graph.add_edge("Vizela", "Ponte de Lima", 80, "asfalto", restricoes=[])
    graph.add_edge("Ponte de Lima", "Vizela", 80, "asfalto", restricoes=[])
    graph.add_edge("Porto", "Guimarães", 70, "asfalto", restricoes=[])
    graph.add_edge("Guimarães", "Porto", 70, "asfalto", restricoes=[])
    graph.add_edge("Porto", "Braga", 60, "asfalto", restricoes=["drone"])
    graph.add_edge("Braga", "Porto", 60, "asfalto", restricoes=["drone"])
    graph.add_edge("Lisboa", "Coimbra", 200, "terra", restricoes=["camião"])
    graph.add_edge("Coimbra", "Lisboa", 200, "terra", restricoes=["camião"])
    graph.add_edge("Coimbra", "Aveiro", 50, "paralelo", restricoes=[])
    graph.add_edge("Aveiro", "Coimbra", 50, "paralelo", restricoes=[])
    graph.add_edge("Aveiro", "Braga", 120, "asfalto", restricoes=["camião"])
    graph.add_edge("Braga", "Aveiro", 120, "asfalto", restricoes=["camião"])
    graph.add_edge("Ponte de Lima", "Lisboa", 365, "paralelo", restricoes=["drone"])
    graph.add_edge("Lisboa", "Ponte de Lima", 365, "paralelo", restricoes=["drone"])
    graph.add_edge("Aveiro", "Porto", 70, "asfalto", restricoes=[])
    graph.add_edge("Porto", "Aveiro", 70, "asfalto", restricoes=[])
    graph.add_edge("Lisboa", "Évora", 130, "terra", restricoes=["camião"])
    graph.add_edge("Évora", "Lisboa", 130, "terra", restricoes=["camião"])
    graph.add_edge("Évora", "Faro", 200, "asfalto", restricoes=[])
    graph.add_edge("Faro", "Évora", 200, "asfalto", restricoes=[])
    graph.add_edge("Faro", "Lisboa", 280, "paralelo", restricoes=[])
    graph.add_edge("Lisboa", "Faro", 280, "paralelo", restricoes=[])
    graph.add_edge("Évora", "Porto", 400, "asfalto", restricoes=[])
    graph.add_edge("Porto", "Évora", 400, "asfalto", restricoes=[])

    display_main_menu(graph)
