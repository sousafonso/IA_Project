def heuristic(node, goal):
    urgency_factor = 1 / (node.urgencia + 1)  
    return urgency_factor

