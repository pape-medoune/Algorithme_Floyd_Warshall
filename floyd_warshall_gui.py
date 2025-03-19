import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math

from floyd_warshall_algorithm import floyd_warshall, reconstruct_path
from graph_visualization import draw_graph
from gui_components import configure_styles, create_dialog, create_text_tags, add_node_dialog, remove_node_dialog, \
    add_edge_dialog, find_path_dialog


class FloydWarshallGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithme de Floyd-Warshall")

        # Mettre la fenêtre en plein écran
        self.root.state('zoomed')  # Pour Windows

        # Initialisation du graphe
        self.G = nx.DiGraph()
        self.node_positions = {}
        self.inf = float('inf')

        # Configuration des styles
        configure_styles()

        # Création de l'interface
        self.create_widgets()

        # Graphe d'exemple par défaut
        self.create_example_graph()

    def create_widgets(self):
        # Frame principale
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        # Frame gauche (contrôles)
        left_frame = ttk.LabelFrame(main_frame, text="Contrôles")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=15, pady=15)

        # Boutons pour la gestion du graphe avec style amélioré
        btn_width = 25  # Largeur fixe pour tous les boutons
        padding = 20  # Espacement vertical entre les boutons

        # Créer des cadres pour organiser les boutons par catégorie
        nodes_frame = ttk.LabelFrame(left_frame, text="Gestion des Sommets")
        nodes_frame.pack(fill=tk.X, padx=10, pady=10)

        edges_frame = ttk.LabelFrame(left_frame, text="Gestion des Arcs")
        edges_frame.pack(fill=tk.X, padx=10, pady=10)

        graph_frame = ttk.LabelFrame(left_frame, text="Gestion du Graphe")
        graph_frame.pack(fill=tk.X, padx=10, pady=10)

        algo_frame = ttk.LabelFrame(left_frame, text="Algorithme")
        algo_frame.pack(fill=tk.X, padx=10, pady=10)

        # Boutons pour les sommets
        ttk.Button(nodes_frame, text="Ajouter un sommet", command=self.add_node,
                   width=btn_width).pack(fill=tk.X, padx=10, pady=padding)
        ttk.Button(nodes_frame, text="Supprimer un sommet", command=self.remove_node,
                   style='Delete.TButton', width=btn_width).pack(fill=tk.X, padx=10, pady=padding)

        # Boutons pour les arcs
        ttk.Button(edges_frame, text="Ajouter un arc", command=self.add_edge,
                   width=btn_width).pack(fill=tk.X, padx=10, pady=padding)
        ttk.Button(edges_frame, text="Supprimer un arc", command=self.remove_edge,
                   style='Delete.TButton', width=btn_width).pack(fill=tk.X, padx=10, pady=padding)

        # Boutons pour le graphe
        ttk.Button(graph_frame, text="Graphe d'exemple", command=self.create_example_graph,
                   width=btn_width).pack(fill=tk.X, padx=10, pady=padding)
        ttk.Button(graph_frame, text="Effacer le graphe", command=self.clear_graph,
                   style='Delete.TButton', width=btn_width).pack(fill=tk.X, padx=10, pady=padding)

        # Boutons pour l'algorithme
        ttk.Button(algo_frame, text="Exécuter Floyd-Warshall",
                   command=self.run_floyd_warshall, style='Accent.TButton',
                   width=btn_width).pack(fill=tk.X, padx=10, pady=padding)
        ttk.Button(algo_frame, text="Rechercher un chemin",
                   command=self.find_path, width=btn_width).pack(fill=tk.X, padx=10, pady=padding)

        # Frame centrale pour le graphe
        self.graph_frame = ttk.LabelFrame(main_frame, text="Graphe")
        self.graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Frame droite (résultats)
        right_frame = ttk.LabelFrame(main_frame, text="Résultats")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15, ipadx=15, ipady=15)

        # Zone de texte pour afficher les matrices (police plus grande)
        self.result_text = tk.Text(right_frame, wrap=tk.WORD, width=50, font=('Courier New', 18))
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Configuration des tags pour le formatage du texte
        create_text_tags(self.result_text)

        # Initialisation de la figure pour le graphe (plus grande)
        self.fig, self.ax = plt.subplots(figsize=(10, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    def create_example_graph(self):
        # Effacer le graphe existant
        self.clear_graph()

        # Ajouter des sommets
        nodes = ['A', 'B', 'C', 'D']
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / len(nodes)
            x = math.cos(angle)
            y = math.sin(angle)
            self.G.add_node(node)
            self.node_positions[node] = (x, y)

        # Ajouter des arcs avec poids
        edges = [('A', 'B', 5), ('B', 'C', 3), ('C', 'D', 1), ('A', 'D', 10)]
        for u, v, w in edges:
            self.G.add_edge(u, v, weight=w)

        # Mettre à jour l'affichage
        self.draw_graph()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END,
                                "Graphe d'exemple créé. Cliquez sur 'Exécuter Floyd-Warshall' pour calculer les plus courts chemins.")

    def clear_graph(self):
        self.G.clear()
        self.node_positions.clear()
        self.draw_graph()
        self.result_text.delete(1.0, tk.END)

    def add_node(self):
        def on_validate(node):
            # Placer le nouveau sommet au hasard sur le cercle
            angle = 2 * math.pi * np.random.random()
            x = math.cos(angle)
            y = math.sin(angle)
            self.G.add_node(node)
            self.node_positions[node] = (x, y)
            self.draw_graph()

        add_node_dialog(self.root, on_validate, self.G.nodes())

    def remove_node(self):
        if not self.G.nodes():
            messagebox.showinfo("Information", "Le graphe est vide.")
            return

        def on_validate(node):
            self.G.remove_node(node)
            if node in self.node_positions:
                del self.node_positions[node]
            self.draw_graph()

        remove_node_dialog(self.root, on_validate, list(self.G.nodes()))

    def add_edge(self):
        if len(self.G.nodes()) < 2:
            messagebox.showinfo("Information", "Ajoutez au moins deux sommets d'abord.")
            return

        def on_validate(source, target, weight):
            self.G.add_edge(source, target, weight=weight)
            self.draw_graph()

        add_edge_dialog(self.root, on_validate, list(self.G.nodes()))

    def remove_edge(self):
        if not self.G.edges():
            messagebox.showinfo("Information", "Le graphe ne contient pas d'arcs.")
            return

        # Créer une boîte de dialogue personnalisée
        dialog = tk.Toplevel(self.root)
        dialog.title("Supprimer un arc")
        dialog.geometry("500x260")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # Personnaliser l'apparence
        dialog.configure(background='#f0f0f0')

        # Centrer la fenêtre
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        # Cadre pour les widgets
        frame = ttk.Frame(dialog, padding=25)
        frame.pack(fill=tk.BOTH, expand=True)

        # Variables pour stocker les valeurs
        source_var = tk.StringVar()
        target_var = tk.StringVar()

        # Liste des arcs existants pour créer des listes déroulantes
        edges_dict = {}
        for u, v in self.G.edges():
            if u not in edges_dict:
                edges_dict[u] = []
            edges_dict[u].append(v)

        source_nodes = sorted(edges_dict.keys())

        # Labels et champs
        ttk.Label(frame, text="Sommet de départ:", font=('Arial', 16)).grid(row=0, column=0, sticky='w', pady=(0, 10))
        source_combo = ttk.Combobox(frame, textvariable=source_var, values=source_nodes,
                                    font=('Arial', 16), width=20, state="readonly")
        source_combo.grid(row=0, column=1, sticky='w', pady=(0, 20))
        if source_nodes:
            source_combo.current(0)

        ttk.Label(frame, text="Sommet d'arrivée:", font=('Arial', 16)).grid(row=1, column=0, sticky='w', pady=(0, 10))
        target_combo = ttk.Combobox(frame, textvariable=target_var,
                                    font=('Arial', 16), width=20, state="readonly")
        target_combo.grid(row=1, column=1, sticky='w', pady=(0, 20))

        # Message d'état
        status_var = tk.StringVar()
        status_label = ttk.Label(frame, textvariable=status_var,
                                 font=('Arial', 14), foreground='red')
        status_label.grid(row=2, column=0, columnspan=2, sticky='w', pady=(0, 15))

        # Fonction pour mettre à jour la liste des cibles en fonction de la source sélectionnée
        def update_targets(*args):
            source = source_var.get()
            if source in edges_dict:
                target_nodes = edges_dict[source]
                target_combo['values'] = target_nodes
                if target_nodes:
                    target_combo.current(0)
            else:
                target_combo['values'] = []
                target_var.set('')

        # Lier la fonction à la sélection de la source
        source_var.trace('w', update_targets)

        # Initialiser la liste des cibles
        if source_nodes:
            update_targets()

        # Fonction de validation
        def validate():
            source = source_var.get()
            target = target_var.get()

            if not source or not target:
                status_var.set("Erreur: Sélectionnez les sommets de départ et d'arrivée.")
                return

            if self.G.has_edge(source, target):
                self.G.remove_edge(source, target)
                self.draw_graph()
                dialog.destroy()
            else:
                status_var.set(f"Erreur: L'arc de '{source}' à '{target}' n'existe pas.")

        # Boutons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(15, 0))

        cancel_btn = ttk.Button(btn_frame, text="Annuler", command=dialog.destroy,
                                width=12)
        cancel_btn.pack(side=tk.LEFT, padx=15)

        delete_btn = ttk.Button(btn_frame, text="Supprimer", command=validate,
                                style='Delete.TButton', width=12)
        delete_btn.pack(side=tk.RIGHT, padx=15)

        # Attendre que le dialogue soit fermé
        self.root.wait_window(dialog)

    def draw_graph(self):
        self.ax.clear()

        # Utiliser la fonction du module graph_visualization
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in self.G.edges(data=True)}
        draw_graph(self.ax, self.G, self.node_positions, edge_labels=edge_labels)

        self.canvas.draw()

    def run_floyd_warshall(self):
        if not self.G.nodes():
            messagebox.showinfo("Information", "Le graphe est vide.")
            return

        # Convertir le graphe en matrice d'adjacence
        nodes = list(self.G.nodes())
        n = len(nodes)

        # Créer un dictionnaire pour mapper les noms des nœuds à leurs indices
        node_to_idx = {node: i for i, node in enumerate(nodes)}

        # Initialiser la matrice d'adjacence avec inf pour les arcs manquants
        adj_matrix = [[self.inf for _ in range(n)] for _ in range(n)]

        # Remplir la diagonale avec des zéros (distance d'un nœud à lui-même)
        for i in range(n):
            adj_matrix[i][i] = 0

        # Remplir la matrice avec les poids des arcs
        for u, v, data in self.G.edges(data=True):
            i, j = node_to_idx[u], node_to_idx[v]
            adj_matrix[i][j] = data['weight']

        # Exécuter l'algorithme de Floyd-Warshall
        distances, predecessors = floyd_warshall(adj_matrix, self.inf)

        # Afficher les résultats
        self.display_results(nodes, distances, predecessors)

        # Stocker les résultats pour une utilisation ultérieure
        self.nodes = nodes
        self.distances = distances
        self.predecessors = predecessors
        self.node_to_idx = node_to_idx

    def display_results(self, nodes, distances, predecessors):
        """Affiche les résultats de l'algorithme de Floyd-Warshall avec un formatage amélioré"""
        n = len(nodes)

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Matrice des distances minimales :\n\n", "title")

        # Calculer la largeur nécessaire pour chaque colonne (basée sur le contenu)
        col_width = 7  # Largeur minimale par défaut

        # Afficher les en-têtes de colonnes avec un espacement uniforme
        self.result_text.insert(tk.END, "     ")  # Espace pour la 1ère colonne (labels des lignes)
        for j in range(n):
            self.result_text.insert(tk.END, f"{nodes[j]:^{col_width}}")
        self.result_text.insert(tk.END, "\n")

        # Afficher une ligne de séparation
        self.result_text.insert(tk.END, "   " + "─" * (col_width * n + n) + "\n")

        # Afficher les distances avec les noms des sommets
        for i in range(n):
            self.result_text.insert(tk.END, f"{nodes[i]} | ")
            for j in range(n):
                if distances[i][j] == self.inf:
                    self.result_text.insert(tk.END, f"{'∞':^{col_width - 1}} ", "inf")
                else:
                    value = f"{distances[i][j]:.1f}"
                    self.result_text.insert(tk.END, f"{value:^{col_width - 1}} ", "normal")
            self.result_text.insert(tk.END, "\n")

        self.result_text.insert(tk.END,
                                "\nUtilisez 'Rechercher un chemin' pour trouver le plus court chemin entre deux sommets.\n",
                                "instruction")
    def find_path(self):
        if not hasattr(self, 'distances'):
            messagebox.showinfo("Information", "Exécutez d'abord l'algorithme de Floyd-Warshall.")
            return

        def on_validate(source, target):
            # Conversion des noms de nœuds en indices
            i = self.node_to_idx[source]
            j = self.node_to_idx[target]

            # Vérifier s'il existe un chemin
            if self.distances[i][j] == self.inf:
                return False

            # Reconstituer le chemin
            path_indices = reconstruct_path(self.predecessors, i, j)
            path_nodes = [self.nodes[idx] for idx in path_indices]

            # Afficher le résultat
            self.result_text.insert(tk.END, "\n\n")
            self.result_text.insert(tk.END, f"Chemin le plus court de '{source}' à '{target}':\n\n", "path_title")

            # Afficher le chemin
            for idx, node in enumerate(path_nodes):
                self.result_text.insert(tk.END, node, "path_node")
                if idx < len(path_nodes) - 1:
                    self.result_text.insert(tk.END, " → ", "arrow")

            # Afficher la distance
            self.result_text.insert(tk.END, f"\n\nDistance totale: {self.distances[i][j]:.1f}\n", "distance")

            # Mettre à jour l'affichage du graphe pour montrer le chemin
            self.highlight_path(path_nodes)

            # Défiler jusqu'à la fin
            self.result_text.see(tk.END)

            return True

        find_path_dialog(self.root, on_validate, self.nodes)

    def highlight_path(self, path_nodes):
        """
        Met en évidence le chemin trouvé dans le graphe.
        """
        self.ax.clear()

        # Utiliser la fonction du module graph_visualization
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in self.G.edges(data=True)}
        draw_graph(self.ax, self.G, self.node_positions, edge_labels=edge_labels, highlight_path=path_nodes)

        # Mettre à jour le titre
        self.ax.set_title("Chemin le plus court mis en évidence", fontsize=22, pad=25, fontweight='bold')
        self.canvas.draw()