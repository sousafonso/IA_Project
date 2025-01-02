def heuristic(node, goal, graph):
    """
    Calcula a heurística entre dois nós com base em urgência e acessibilidade.
    :param node: Nome do nó inicial.
    :param goal: Nome do nó objetivo.
    :param graph: Objeto do grafo que contém as localidades.
    :return: Valor da heurística.
    """
    # Obter os objetos Localidade para o nó e o objetivo
    node_obj = graph.get_node(node)
    goal_obj = graph.get_node(goal)

    if not node_obj or not goal_obj:
        raise ValueError(f"Nós inválidos: {node} ou {goal} não existem no grafo.")

    # Fator de urgência
    urgency_factor = abs(node_obj.urgencia - goal_obj.urgencia)

    # Penalidade por acessibilidade
    accessibility_penalty = {
        "asfalto": 0,
        "paralelo": 5,
        "terra": 10
    }.get(node_obj.acessibilidade, 10)  # Penalidade padrão para pavimentos desconhecidos

    # Retorna a heurística como uma combinação ponderada dos fatores
    return urgency_factor * pavement_factor
