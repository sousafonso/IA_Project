import os
from modelos.localidade import Localidade
from modelos.rota import Rota
from modelos.grafo import Grafo
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
    clear_screen()
    print("\nVisualizando o Grafo:")
    visualize_graph_with_image(graph)
    input("\nPressione Enter para voltar ao menu...")



def display_algorithm_menu(graph):
    """
    Exibe o menu para escolha de algoritmos.
    """
    while True:
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
    Executa o algoritmo selecionado.
    :param algorithm: Nome do algoritmo.
    :param graph: Objeto Grafo.
    """
    clear_screen()
    print(f"\nExecutando {algorithm}...")
    start = input("Digite o nó de início: ")
    goal = input("Digite o nó objetivo: ")

    if algorithm == "BFS":
        result = bfs(graph, start, goal)
    elif algorithm == "DFS":
        result = dfs(graph, start, goal)
    elif algorithm == "A*":
        result = a_star(graph, start, goal, heuristic)
    elif algorithm == "Greedy Search":
        result = greedy_search(graph, start, goal, heuristic)
    elif algorithm == "Custo Uniforme":
        result = uniform_cost_search(graph, start, goal)
    else:
        print("Algoritmo não reconhecido.")
        return

    clear_screen()
    if result:
        print(f"Caminho encontrado: {' -> '.join(result)}")
    else:
        print("Não foi possível encontrar um caminho.")

if __name__ == "__main__":
    # Criar localidades
    loc_a = Localidade("Guimarães", populacao=500, urgencia=3, acessibilidade="asfalto")
    loc_b = Localidade("Braga", populacao=300, urgencia=5, acessibilidade="terra")
    loc_c = Localidade("Fafe", populacao=800, urgencia=2, acessibilidade="trilha")
    loc_d = Localidade("Vizela", populacao=1000, urgencia=1, acessibilidade="asfalto")
    loc_e = Localidade("Ponte de Lima", populacao=200, urgencia=4, acessibilidade="terra")

    # Criar o grafo
    graph = Grafo()

    # Adicionar localidades ao grafo
    for loc in [loc_a, loc_b, loc_c, loc_d, loc_e]:
        graph.add_node(loc)

    # Adicionar rotas entre localidades
    graph.add_edge("Guimarães", "Braga", 50, "asfalto", restricoes=["camião", "drone"])
    graph.add_edge("Guimarães", "Fafe", 70, "terra", restricoes=["drone"])
    graph.add_edge("Braga", "Vizela", 40, "trilha", restricoes=["helicóptero"])
    graph.add_edge("Fafe", "Ponte de Lima", 60, "terra", restricoes=["camião"])
    graph.add_edge("Vizela", "Ponte de Lima", 80, "asfalto", restricoes=[])

    # Exibir o menu principal
    display_main_menu(graph)
