def heuristic(node, goal):
    # Inverter o fator de urgência para priorizar localidades com maior urgência
    urgency_factor = 1 / (node.urgencia + 1)  # Adiciona 1 para evitar divisão por zero
    return urgency_factor

