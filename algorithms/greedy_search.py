# Greedy Search
def greedy_search(graph, start, goal, transport):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start.id: None}
    
    while not frontier.empty():
        _, current = frontier.get()

        if current.id == goal.id:
            break
        
        for neighbor in graph.get_neighbors(current):
            route = graph.get_route(current, neighbor)
            if neighbor.id not in came_from and transport.can_access_route(route) and transport.can_complete_route(route.distance):
                priority = heuristic(neighbor, goal) - neighbor.urgency
                frontier.put((priority, neighbor))
                came_from[neighbor.id] = current.id
                transport.update_fuel(route.distance)

    return reconstruct_path(came_from, start.id, goal.id) if goal.id in came_from else None

def reconstruct_path(came_from, start_id, goal_id):
    current_id = goal_id
    path = []
    while current_id != start_id:
        path.append(current_id)
        current_id = came_from[current_id]
    path.append(start_id)
    path.reverse()
    return path
