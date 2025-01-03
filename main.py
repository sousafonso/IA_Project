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

"""Tipo de pavimento só importa no camião"""
"""Quantidade de mantimentos e combustível"""


def clear_screen():
    """
    Limpa o terminal para que o menu anterior desapareça.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def display_main_menu(graph):
    """
    Exibe o menu principal para o usuário.
    """
    while True:
        print("\nMenu Principal:")
        print("1. Visualizar Grafo")
        print("2. Escolher Algoritmo de Procura")
        print("0. Sair")

        try:
            option = int(input("Escolha uma opção: "))
            if option == 1:
                visualize_graph(graph)
            elif option == 2:
                display_algorithm_menu(graph)
            elif option == 0:
                print("Saindo do programa.")
                break
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")

def visualize_graph(graph):
    clear_screen()
    print("\nVisualizando o Grafo:")
    visualize_graph_with_image(graph)
    input("\nPressione Enter para voltar ao menu...")

def display_algorithm_menu(graph):
    """
    Exibe o menu para escolha de algoritmos.
    """
    while True:
        simulate_events(graph)
        clear_screen()

        print("\nEscolha o Algoritmo de Procura:")
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
                print("Voltando ao Menu Principal.")
                break
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")

def execute_algorithm(algorithm, graph):
    """
    Executa o algoritmo selecionado e realiza simulações controladas.
    :param algorithm: Nome do algoritmo.
    :param graph: Objeto Grafo.
    """
    clear_screen()
    print(f"\nExecutando {algorithm}...")
    start = input("Digite o nó de início: ").strip()

    if not graph.get_node(start):
        print(f"O nó '{start}' não existe no grafo.")
        input("\nPressione Enter para voltar ao menu...")
        return
    
    # Simular eventos no grafo
    simulated_changes = simulate_events(graph, reduce_probability=True)
    print("\n--- Alterações Iniciais ---")
    for change in simulated_changes:
        print(change)

    veiculos = {
        "camião": Transporte("camião", 5000, 60, 500),
        "drone": Transporte("drone", 600, 80, 100),
        "helicóptero": Transporte("helicóptero", 2000, 120, 1000),
    }

    results = []
    for vehicle, transporte in veiculos.items():
        print(f"\nCalculando o melhor caminho para o veículo: {vehicle}")
        graph_state_backup = {node.nome: node.mantimentos for node in graph.nodes.values()}  # Backup do estado do grafo
        graph.update_costs_for_vehicle(transporte.getVelocidade())

        # Alterações em cada nó visitado
        path = []

        if algorithm == "BFS":
            path, cost = bfs(graph, start, transporte)
        elif algorithm == "DFS":
            path, cost = dfs(graph, start, transporte)
       # elif algorithm == "A*":
       #     path, cost = a_star(graph, start, goal, heuristic, transporte)
       # elif algorithm == "Greedy Search":
       #     path, cost = greedy_search(graph, start, goal, heuristic, transporte)
       # elif algorithm == "Custo Uniforme":
       #     path, cost = uniform_cost_search(graph, start, goal, transporte)
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
            results.append((vehicle, path, cost, total_entregue))
            print(f"Veículo: {vehicle.capitalize()}, Caminho: {' -> '.join(path)}, Custo: {cost} horas, Mantimentos entregues: {total_entregue}")
        else:
            print(f"Não foi possível encontrar um caminho para o veículo: {vehicle.capitalize()}")

        graph.restore_original_costs()

    if results:
        best_vehicle = min(
            results, key=lambda x: (x[2] / x[3], x[2]) if x[3] > 0 else (float('inf'), float('inf'))
        )
        print(f"\nMelhor veículo: {best_vehicle[0].capitalize()}, Caminho: {' -> '.join(best_vehicle[1])}, Custo: {best_vehicle[2]} horas, Mantimentos entregues: {best_vehicle[3]}")
    else:
        print("\nNenhum veículo conseguiu encontrar um caminho válido.")

    input("\nPressione Enter para voltar ao menu...")


def simulate_events(graph, reduce_probability=True):
    """
    Simula eventos aleatórios no grafo, como bloqueio de rotas e alteração de urgências.
    Esta função pode ser chamada uma vez para criar um estado inicial fixo.

    :param graph: Objeto do grafo.
    :param reduce_probability: Reduz a probabilidade de alterações (default=True).
    :return: Lista de alterações aplicadas.
    """
    alterations = []

    print("\n--- Simulação de Eventos Aleatórios ---")

    # Bloquear rotas aleatoriamente devido a imprevistos
    for (origem, destino), route in graph.edges.items():
        if reduce_probability:
            prob_tempestade = 0.1  # 10% de chance
            prob_estrada = 0.15  # 15% de chance
        else:
            prob_tempestade = 0.2
            prob_estrada = 0.3

        imprevisto = random.choice(["tempestade", "estrada bloqueada", None])  # Escolhe um evento aleatório
        if imprevisto == "tempestade" and random.random() < prob_tempestade:
            route.update_blockage("tempestade")
            alterations.append(f"Rota de {origem} para {destino} foi bloqueada devido a uma tempestade.")
        elif imprevisto == "estrada bloqueada" and random.random() < prob_estrada:
            route.update_blockage("estrada bloqueada")
            alterations.append(f"Rota de {origem} para {destino} foi marcada como 'estrada bloqueada'.")

    # Alterar urgência de localidades aleatoriamente
    for node in graph.nodes.values():
        if random.random() < 0.2:  # 20% de chance de mudar a urgência
            old_urgency = node.urgencia
            node.urgencia = random.randint(1, 5)  # Nova urgência entre 1 e 5
            alterations.append(f"Urgência de {node.nome} mudou de {old_urgency} para {node.urgencia}.")

    print("\n--- Fim da Simulação ---")

    return alterations



if __name__ == "__main__":
    # Criar localidades com nova população e mantimentos
    loc_a = Localidade("Guimarães", populacao=2000, urgencia=3, acessibilidade="asfalto", reabastecimento=True)
    loc_b = Localidade("Braga", populacao=1500, urgencia=5, acessibilidade="terra")
    loc_c = Localidade("Fafe", populacao=1200, urgencia=2, acessibilidade="trilha", reabastecimento=True)
    loc_d = Localidade("Vizela", populacao=1800, urgencia=1, acessibilidade="asfalto")
    loc_e = Localidade("Ponte de Lima", populacao=900, urgencia=4, acessibilidade="terra", reabastecimento=True)
    loc_f = Localidade("Porto", populacao=214349, urgencia=2, acessibilidade="asfalto", reabastecimento=True)
    loc_g = Localidade("Lisboa", populacao=504718, urgencia=1, acessibilidade="paralelo")
    loc_h = Localidade("Coimbra", populacao=143396, urgencia=4, acessibilidade="terra", reabastecimento=True)
    loc_i = Localidade("Aveiro", populacao=78000, urgencia=3, acessibilidade="asfalto")
    loc_j = Localidade("Évora", populacao=56500, urgencia=2, acessibilidade="terra", reabastecimento=True)
    loc_k = Localidade("Faro", populacao=118000, urgencia=3, acessibilidade="asfalto")

    # Adicionar mantimentos atualizados
    loc_a.mantimentos = 500
    loc_b.mantimentos = 400
    loc_c.mantimentos = 300
    loc_d.mantimentos = 250
    loc_e.mantimentos = 600
    loc_f.mantimentos = 350
    loc_g.mantimentos = 200
    loc_h.mantimentos = 400
    loc_i.mantimentos = 150
    loc_j.mantimentos = 200
    loc_k.mantimentos = 400

    # Criar o grafo
    graph = Grafo()

    # Adicionar localidades ao grafo
    for loc in [loc_a, loc_b, loc_c, loc_d, loc_e, loc_f, loc_g, loc_h, loc_i, loc_j, loc_k]:
        graph.add_node(loc)

    # Adicionar rotas entre localidades
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

    # Exibir o menu principal
    display_main_menu(graph)
