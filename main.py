import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from floyd_warshall_algorithm import floyd_warshall, reconstruct_path
from graph_visualization import draw_graph
from gui_components import configure_styles, create_dialog
from floyd_warshall_gui import FloydWarshallGUI

def main():
    root = tk.Tk()
    app = FloydWarshallGUI(root)
    root.mainloop()

# Vous pouvez garder la classe FloydWarshallGUI en important les fonctions des modules

if __name__ == "__main__":
    main()