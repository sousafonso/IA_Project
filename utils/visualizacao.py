import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph_with_image(graph):
    """
    Exibe o grafo como uma imagem usando NetworkX e Matplotlib.
    :param graph: Objeto do grafo (implementação personalizada).
    """
    # Criar um grafo direcionado usando NetworkX
    nx_graph = nx.DiGraph()

    # Adicionar nós ao grafo
    for node_id, node in graph.nodes.items():
        nx_graph.add_node(node_id, label=f"{node_id}\nUrgência: {node.urgencia}")

    # Adicionar arestas ao grafo
    for (origin, destination), route in graph.edges.items():
        label = f"{route.distancia} km\n{route.pavimento}"
        nx_graph.add_edge(origin, destination, label=label, color='red' if route.bloqueado else 'black')

    # Configurar layout e desenhar o grafo
    pos = nx.spring_layout(nx_graph)  # Layout para os nós
    edge_labels = nx.get_edge_attributes(nx_graph, 'label')
    edge_colors = [nx_graph[u][v]['color'] for u, v in nx_graph.edges()]

    # Desenhar o grafo com NetworkX
    plt.figure(figsize=(10, 8))
    nx.draw(nx_graph, pos, with_labels=True, node_size=3000, node_color='lightblue',
            font_size=10, font_weight='bold', edge_color=edge_colors)
    nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=edge_labels, font_color='green')

    # Exibir o grafo na tela
    plt.show()
