import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph_with_image(graph):

    nx_graph = nx.DiGraph()

    for node_id, node in graph.nodes.items():
        nx_graph.add_node(node_id, label=f"{node_id}\nUrgência: {node.urgencia}")

    for (origin, destination), route in graph.edges.items():
        label = f"{route.distancia} km\n{route.pavimento}"
        nx_graph.add_edge(origin, destination, label=label, color='red' if route.bloqueado else 'black')

    pos = nx.spring_layout(nx_graph)  
    edge_labels = nx.get_edge_attributes(nx_graph, 'label')
    edge_colors = [nx_graph[u][v]['color'] for u, v in nx_graph.edges()]

    plt.figure(figsize=(10, 8))
    nx.draw(nx_graph, pos, with_labels=True, node_size=3000, node_color='lightblue',
            font_size=10, font_weight='bold', edge_color=edge_colors)
    nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels, font_color='green')

    plt.show()
