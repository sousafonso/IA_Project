def heuristic(node, goal):
    """
    Calcula a heurística ajustada para considerar apenas a urgência.
    :param node: Objeto Localidade atual.
    :param goal: Objeto Localidade objetivo.
    :return: Valor heurístico ajustado.
    """
    # Inverter o fator de urgência para priorizar localidades com maior urgência
    urgency_factor = 1 / (node.urgencia + 1)  # Adiciona 1 para evitar divisão por zero
    return urgency_factor

