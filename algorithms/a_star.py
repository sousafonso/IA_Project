from queue import PriorityQueue
from models.graph import Graph
from models.locality import Locality
from models.route import Route
from models.transport import Transport

def heuristic(current: Locality, goal: Locality):
    return ((current.x - goal.x) ** 2 + (current.y - goal.y) ** 2) ** 0.5  # Distância euclidiana

def a_star(graph: Graph, start: Locality, goal: Locality, transport: Transport):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start.id: None}
    cost_so_far = {start.id: 0}
    
    while not frontier.empty():
        _, current = frontier.get()
        
        if current.id == goal.id:
            break
        
        for neighbor in graph.get_neighbors(current):
            route = graph.get_route(current, neighbor)
            if transport.can_access_route(route) and transport.can_complete_route(route.distance):
                new_cost = cost_so_far[current.id] + route.get_cost()
                if neighbor.id not in cost_so_far or new_cost < cost_so_far[neighbor.id]:
                    cost_so_far[neighbor.id] = new_cost
                    priority = new_cost + heuristic(neighbor, goal) - neighbor.urgency
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