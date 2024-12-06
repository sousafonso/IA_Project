from models.graph import Graph
from models.locality import Locality
from models.route import Route
from models.transport import Transport

def dfs(graph: Graph, start: Locality, goal: Locality, transport: Transport):
    stack = [start]
    came_from = {start.id: None}
    
    while stack:
        current = stack.pop()
        
        if current.id == goal.id:
            break
        
        for neighbor in graph.get_neighbors(current):
            route = graph.get_route(current, neighbor)
            if neighbor.id not in came_from and transport.can_access_route(route) and transport.can_complete_route(route.distance):
                stack.append(neighbor)
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