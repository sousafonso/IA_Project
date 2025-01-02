def heuristic(node, goal):
    # Fator de urgência: Quanto maior a urgência do nó objetivo, menor o custo estimado.
    urgency_factor = abs(node["urgency"] - goal["urgency"])
    
    # Penalidade por acessibilidade: Nós com pavimento mais difícil têm custo maior.
    accessibility_penalty = {
        "asfalto": 0,
        "paralelo": 5,
        "terra": 10
    }.get(node["accessibility"], 10)  # Penalidade padrão para pavimentos desconhecidos

    # Soma dos fatores
    return urgency_factor + accessibility_penalty
