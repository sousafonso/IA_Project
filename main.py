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
    """clear_screen()"""
    print("\nVisualizando o Grafo:")
    visualize_graph_with_image(graph)
    input("\nPressione Enter para voltar ao menu...")



def display_algorithm_menu(graph):
    """
    Exibe o menu para escolha de algoritmos.
    """
    while True:
        """clear_screen()"""
        simulate_events(graph)
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
    Executa o algoritmo selecionado.
    :param algorithm: Nome do algoritmo.
    :param graph: Objeto Grafo.
    """
    """clear_screen()"""
    print(f"\nExecutando {algorithm}...")
    start = input("Digite o nó de início: ")
    goal = input("Digite o nó objetivo: ")


    if not graph.get_node(start):
        print(f"O nó '{start}' não existe no grafo.")
        input("\nPressione Enter para voltar ao menu...")
        return
    if not graph.get_node(goal):
        print(f"O nó '{goal}' não existe no grafo.")
        input("\nPressione Enter para voltar ao menu...")
        return
    
    transport = Transporte(tipo="camião", capacidade=1000, velocidade=80, autonomia=500)

    path = None
    cost = None

    if algorithm == "BFS":
        path,cost = bfs(graph, start, goal, transport)
    elif algorithm == "DFS":
        path = dfs(graph, start, goal, transport)
    elif algorithm == "A*":
        path = a_star(graph, start, goal, heuristic, transport)
    elif algorithm == "Greedy Search":
        path = greedy_search(graph, start, goal, heuristic, transport)
    elif algorithm == "Custo Uniforme":
        path = uniform_cost_search(graph, start, goal, transport)
    else:
        print("Algoritmo não reconhecido.")
        return

    """clear_screen()"""
    if path:
        print(f"Caminho encontrado: {' -> '.join(path)}")
        if cost is not None:
            print(f"Custo total: {cost} km")
    else:
        print("Não foi possível encontrar um caminho.")


def simulate_events(graph):
    """
    Simula eventos aleatórios, como bloqueio de rotas por tempestades ou marcação como estrada bloqueada,
    além de alteração de urgências nas localidades.
    :param graph: Objeto do grafo.
    """
    print("\n--- Simulação de Eventos Aleatórios ---")

    # Bloquear rotas aleatoriamente devido a imprevistos
    for (origem, destino), route in graph.edges.items():
        imprevisto = random.choice(["tempestade", "estrada bloqueada", None])  # Escolhe um evento aleatório
        if imprevisto == "tempestade" and random.random() < 0.2:  # 20% de chance para tempestade
            route.update_blockage("tempestade")
            print(f"Rota de {origem} para {destino} foi bloqueada devido a uma tempestade.")
        elif imprevisto == "estrada bloqueada" and random.random() < 0.3:  # 30% de chance para estrada bloqueada
            route.update_blockage("estrada bloqueada")
            print(f"Rota de {origem} para {destino} foi marcada como 'estrada bloqueada'.")

    # Alterar urgência de localidades aleatoriamente
    for node in graph.nodes.values():
        if random.random() < 0.4:  # 40% de chance de mudar a urgência
            old_urgency = node.urgencia
            node.urgencia = random.randint(1, 5)  # Nova urgência entre 1 e 5
            print(f"Urgência de {node.nome} mudou de {old_urgency} para {node.urgencia}.")

    print("--- Fim da Simulação ---\n")


if __name__ == "__main__":
    # Criar localidades
    loc_a = Localidade("Guimarães", populacao=500, urgencia=3, acessibilidade="asfalto")
    loc_b = Localidade("Braga", populacao=300, urgencia=5, acessibilidade="terra")
    loc_c = Localidade("Fafe", populacao=800, urgencia=2, acessibilidade="trilha")
    loc_d = Localidade("Vizela", populacao=1000, urgencia=1, acessibilidade="asfalto")
    loc_e = Localidade("Ponte de Lima", populacao=200, urgencia=4, acessibilidade="terra")
    loc_f = Localidade("Porto", populacao=214349, urgencia=2, acessibilidade="asfalto")
    loc_g = Localidade("Lisboa", populacao=504718, urgencia=1, acessibilidade="paralelo")
    loc_h = Localidade("Coimbra", populacao=143396, urgencia=4, acessibilidade="terra")
    loc_i = Localidade("Aveiro", populacao=78000, urgencia=3, acessibilidade="asfalto")
    loc_j = Localidade("Évora", populacao=56500, urgencia=2, acessibilidade="terra")
    loc_k = Localidade("Faro", populacao=118000, urgencia=3, acessibilidade="asfalto")

    # Criar o grafo
    graph = Grafo()

    # Adicionar localidades ao grafo
    for loc in [loc_a, loc_b, loc_c, loc_d, loc_e,loc_f, loc_g,loc_h,loc_i,loc_j,loc_k]:
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