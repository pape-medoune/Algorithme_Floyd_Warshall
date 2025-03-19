# Algorithme de Floyd-Warshall - Interface Graphique

Une application desktop interactive pour visualiser et comprendre l'algorithme de Floyd-Warshall pour trouver les plus courts chemins dans un graphe orienté pondéré.

![image](https://github.com/user-attachments/assets/e8b11b81-2354-435a-875d-b2ca197258f5)


## Description

Cette application permet de:
- Créer et modifier des graphes orientés pondérés
- Exécuter l'algorithme de Floyd-Warshall pour calculer les plus courts chemins entre tous les sommets
- Visualiser la matrice des distances minimales obtenue
- Rechercher et afficher le plus court chemin entre deux sommets

L'algorithme de Floyd-Warshall est un algorithme fondamental en théorie des graphes qui permet de trouver les plus courts chemins entre toutes les paires de sommets d'un graphe orienté pondéré.

## Fonctionnalités

- **Gestion des sommets**: Ajouter et supprimer des sommets
- **Gestion des arcs**: Ajouter et supprimer des arcs avec des poids personnalisables
- **Gestion du graphe**: Créer un graphe d'exemple ou effacer le graphe actuel
- **Algorithme**: Exécuter l'algorithme de Floyd-Warshall et rechercher un chemin entre deux sommets
- **Visualisation**: Affichage graphique du graphe et mise en évidence des chemins trouvés
- **Résultats**: Affichage détaillé de la matrice des distances minimales

## Installation

### Prérequis

- Python 3.8 ou supérieur
- Pip (gestionnaire de paquets Python)

### Bibliothèques requises

- tkinter
- networkx
- matplotlib
- numpy

### Étapes d'installation

1. Clonez ce dépôt:
   ```
   git clone https://github.com/pape-medoune/Algorithme_Floyd_Warshall.git
   cd Algorithme_Floyd_Warshall
   ```

2. Créez un environnement virtuel (recommandé):
   ```
   python -m venv .venv
   ```

3. Activez l'environnement virtuel:
   - Sur Windows:
     ```
     .venv\Scripts\activate
     ```
   - Sur macOS/Linux:
     ```
     source .venv/bin/activate
     ```

4. Installez les dépendances:
   ```
   pip install -r requirements.txt
   ```

5. Lancez l'application:
   ```
   python main.py
   ```

## Structure du projet

Le projet est organisé en modules:

- `main.py`: Point d'entrée de l'application
- `floyd_warshall_algorithm.py`: Implémentation de l'algorithme de Floyd-Warshall
- `graph_visualization.py`: Fonctions pour dessiner et visualiser le graphe
- `gui_components.py`: Composants d'interface utilisateur réutilisables
- `floyd_warshall_gui.py`: Classe principale de l'interface graphique

## Utilisation

1. **Création d'un graphe**:
   - Utilisez le bouton "Graphe d'exemple" pour créer un graphe prédéfini, ou
   - Ajoutez des sommets en cliquant sur "Ajouter un sommet"
   - Ajoutez des arcs entre les sommets en cliquant sur "Ajouter un arc"

2. **Exécution de l'algorithme**:
   - Cliquez sur "Exécuter Floyd-Warshall" pour calculer tous les plus courts chemins
   - La matrice des distances minimales s'affiche dans le panneau de droite

3. **Recherche de chemin**:
   - Cliquez sur "Rechercher un chemin" pour trouver le plus court chemin entre deux sommets
   - Sélectionnez les sommets de départ et d'arrivée dans la boîte de dialogue
   - Le chemin trouvé est mis en évidence sur le graphe et les détails sont affichés

## Contribution

Les contributions sont les bienvenues! N'hésitez pas à:
- Signaler des bugs
- Suggérer des améliorations
- Soumettre des pull requests

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Auteur

Développé par Mouhamedoune Fall, Meissa Babou et Mamadou Ba.
