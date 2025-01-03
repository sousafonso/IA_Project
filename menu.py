import os
import shutil

def clear_screen():
    """
    Limpa a tela para o terminal.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_size():
    """
    Retorna o tamanho atual do terminal (linhas e colunas).
    """
    size = shutil.get_terminal_size()
    return size.lines, size.columns

def center_text(text, width):
    """
    Centraliza o texto com base na largura do terminal.
    :param text: Texto a ser centralizado.
    :param width: Largura do terminal.
    :return: Texto centralizado.
    """
    return text.center(width)

def display_menu(options, simulation_text=None, results_text=None):
    """
    Exibe o menu com as opções centralizadas e espaços para a simulação e resultados.
    :param options: Lista de opções para o menu.
    :param simulation_text: Texto a ser exibido no topo, simulando eventos.
    :param results_text: Texto dos resultados a ser exibido na parte inferior.
    """
    clear_screen()
    lines, columns = get_terminal_size()

    # Espaço para simulação no topo
    if simulation_text:
        simulation_output = center_text(simulation_text, columns)
        print(f"\n{simulation_output}\n")

    # Espaço em branco acima do menu
    empty_lines_above_menu = max(0, (lines - len(options) - 5) // 2)
    print("\n" * empty_lines_above_menu)

    # Exibe o menu centralizado
    for option in options:
        print(center_text(option, columns))

    # Espaço abaixo do menu para input
    print("\n")

    # Espaço para os resultados na parte inferior
    if results_text:
        results_output = f"{results_text}".center(columns)
        print("\n" * 2)
        print(results_output)

    # Input do usuário centralizado
    user_input_prompt = "Escolha uma opção: "
    print(center_text(user_input_prompt, columns), end="")
    return input()
