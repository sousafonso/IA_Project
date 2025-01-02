PAVEMENT_FACTORS = {
    "asfalto": 1.0,
    "terra": 1.5,
    "trilha": 2.0,
}

def heuristic(node, goal):
    """
    Calcula a heurística entre o nó atual e o objetivo.
    :param node: Objeto Localidade atual.
    :param goal: Objeto Localidade objetivo.
    :return: Valor heurístico (quanto menor, melhor).
    """
    # Fator baseado na urgência
    urgency_factor = abs(node.urgencia - goal.urgencia)

    # Fator baseado no tipo de pavimento da localidade atual
    pavement_factor = PAVEMENT_FACTORS.get(node.acessibilidade, 1.0)

    # Retorna a heurística como uma combinação ponderada dos fatores
    return urgency_factor * pavement_factor
