def floyd_warshall(graph, inf=float('inf')):
    """
    Implémentation pure de l'algorithme de Floyd-Warshall.

    Paramètres:
    - graph: Matrice d'adjacence représentant le graphe
    - inf: Valeur représentant l'infini

    Retourne:
    - distances: Matrice des plus courtes distances
    - predecessors: Matrice des prédécesseurs pour reconstruire les chemins
    """
    n = len(graph)

    # Initialisation des matrices
    distances = [row[:] for row in graph]
    predecessors = [[None for _ in range(n)] for _ in range(n)]

    # Initialiser les prédécesseurs pour les arcs directs
    for i in range(n):
        for j in range(n):
            if i != j and distances[i][j] < inf:
                predecessors[i][j] = -1

    # Algorithme principal
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if distances[i][k] < inf and distances[k][j] < inf:
                    new_dist = distances[i][k] + distances[k][j]
                    if new_dist < distances[i][j]:
                        distances[i][j] = new_dist
                        predecessors[i][j] = k

    return distances, predecessors


def reconstruct_path(predecessors, i, j):
    """
    Reconstruit le chemin entre les sommets i et j.

    Paramètres:
    - predecessors: Matrice des prédécesseurs
    - i: Indice du sommet de départ
    - j: Indice du sommet d'arrivée

    Retourne:
    - path: Liste des indices des sommets formant le chemin
    """
    if i == j:
        return [i]
    if predecessors[i][j] is None:
        return []

    def build_path(i, j, path):
        k = predecessors[i][j]
        if k is None or k == -1:
            return
        build_path(i, k, path)
        path.append(k)
        build_path(k, j, path)

    path = []
    build_path(i, j, path)
    return [i] + path + [j]