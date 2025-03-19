import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(ax, G, node_positions, edge_labels=None, highlight_path=None):
    """
    Dessine un graphe sur un axe matplotlib.

    Paramètres:
    - ax: Axe matplotlib sur lequel dessiner
    - G: Graphe NetworkX
    - node_positions: Dictionnaire des positions des nœuds
    - edge_labels: Dictionnaire des étiquettes des arcs
    - highlight_path: Liste des nœuds formant un chemin à mettre en évidence
    """
    ax.clear()

    # Dessiner les nœuds normaux
    nx.draw_networkx_nodes(G, node_positions, ax=ax,
                           node_color='#4dabf7', node_size=1000,
                           alpha=0.9, edgecolors='#3b5bdb', linewidths=2)

    # Dessiner les arêtes normales
    nx.draw_networkx_edges(G, node_positions, ax=ax,
                           arrowstyle='->', arrowsize=30,
                           width=3, alpha=0.9, edge_color='#4c6ef5')

    # Ajouter les labels des nœuds
    nx.draw_networkx_labels(G, node_positions, ax=ax, font_size=18,
                            font_weight='bold', font_color='white')

    # Ajouter les poids des arêtes
    if edge_labels:
        nx.draw_networkx_edge_labels(G, node_positions, edge_labels=edge_labels,
                                     ax=ax, font_size=16, font_weight='bold',
                                     bbox=dict(facecolor='white', alpha=0.7,
                                               edgecolor='none', boxstyle='round,pad=0.3'))

    # Mettre en évidence un chemin si fourni
    if highlight_path and len(highlight_path) > 1:
        path_edges = list(zip(highlight_path[:-1], highlight_path[1:]))

        # Dessiner les nœuds du chemin
        nx.draw_networkx_nodes(G, node_positions, ax=ax,
                               nodelist=highlight_path, node_color='#e64980',
                               node_size=1000, alpha=1, edgecolors='#c2255c', linewidths=3)

        # Dessiner les arêtes du chemin
        nx.draw_networkx_edges(G, node_positions, ax=ax,
                               edgelist=path_edges, arrowstyle='->', arrowsize=35,
                               width=4, edge_color='#e64980', alpha=1)

    ax.set_title("Graphe orienté pondéré", fontsize=22, pad=25, fontweight='bold')
    ax.axis('off')