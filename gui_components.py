import tkinter as tk
from tkinter import ttk, messagebox


def configure_styles():
    """Configure les styles pour améliorer l'apparence de l'interface"""
    style = ttk.Style()

    # Style général de l'application
    style.configure('TFrame', background='#f0f0f0')
    style.configure('TLabelframe', background='#f0f0f0', font=('Arial', 16, 'bold'))
    style.configure('TLabelframe.Label', font=('Arial', 16, 'bold'))

    # Styles pour les boutons
    style.configure('TButton', font=('Arial', 16), padding=12)
    style.configure('Accent.TButton', font=('Arial', 18, 'bold'), padding=15)
    style.configure('Delete.TButton', font=('Arial', 16), padding=12, background='#ff5252')

    # Style pour les combobox et les entrées
    style.configure('TCombobox', font=('Arial', 14))
    style.configure('TEntry', font=('Arial', 14))
    style.configure('TSpinbox', font=('Arial', 14))

    # Style pour les labels
    style.configure('TLabel', font=('Arial', 14))
    style.configure('Title.TLabel', font=('Arial', 18, 'bold'))
    style.configure('Dialog.TLabel', font=('Arial', 16))

    return style


def create_text_tags(text_widget):
    """Configure les tags pour le formatage du texte dans un widget Text"""
    text_widget.tag_configure("title", font=("Arial", 18, "bold"))
    text_widget.tag_configure("subtitle", font=("Arial", 16, "bold"), foreground="blue")
    text_widget.tag_configure("instruction", font=("Arial", 16, "italic"), foreground="green")
    text_widget.tag_configure("inf", font=("Arial", 18), foreground="red")
    text_widget.tag_configure("normal", font=("Courier New", 16))
    text_widget.tag_configure("path_title", font=("Arial", 18, "bold"))
    text_widget.tag_configure("path_node", font=("Courier New", 18, "bold"), foreground="blue")
    text_widget.tag_configure("arrow", font=("Arial", 18, "bold"), foreground="green")
    text_widget.tag_configure("distance", font=("Arial", 16, "bold"))


def create_dialog(parent, title, width=400, height=250):
    """Crée une boîte de dialogue standard avec un style cohérent"""
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.geometry(f"{width}x{height}")
    dialog.resizable(False, False)
    dialog.transient(parent)
    dialog.grab_set()

    # Personnaliser l'apparence
    dialog.configure(background='#f0f0f0')

    # Centrer la fenêtre
    dialog.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() - dialog.winfo_width()) // 2
    y = parent.winfo_y() + (parent.winfo_height() - dialog.winfo_height()) // 2
    dialog.geometry(f"+{x}+{y}")

    # Créer un cadre principal
    frame = ttk.Frame(dialog, padding=25)
    frame.pack(fill=tk.BOTH, expand=True)

    return dialog, frame


def add_node_dialog(parent, on_validate, existing_nodes=None):
    """Crée un dialogue pour ajouter un nouveau nœud"""
    dialog, frame = create_dialog(parent, "Ajouter un sommet", 400, 200)

    # Label
    ttk.Label(frame, text="Nom du sommet:", font=('Arial', 16), style='Dialog.TLabel').pack(pady=(0, 15))

    # Champ de saisie
    entry_var = tk.StringVar()
    entry = ttk.Entry(frame, textvariable=entry_var, font=('Arial', 16), width=20)
    entry.pack(pady=(0, 25))
    entry.focus_set()

    # Fonction de validation
    def validate():
        node = entry_var.get().strip()
        if not node:
            return

        if existing_nodes and node in existing_nodes:
            messagebox.showwarning("Avertissement", f"Le sommet '{node}' existe déjà.", parent=dialog)
            return

        on_validate(node)
        dialog.destroy()

    # Boutons
    btn_frame = ttk.Frame(frame)
    btn_frame.pack(fill=tk.X)

    cancel_btn = ttk.Button(btn_frame, text="Annuler", command=dialog.destroy, width=12)
    cancel_btn.pack(side=tk.LEFT, padx=10)

    add_btn = ttk.Button(btn_frame, text="Ajouter", command=validate, style='Accent.TButton', width=12)
    add_btn.pack(side=tk.RIGHT, padx=10)

    # Validation en appuyant sur Entrée
    entry.bind("<Return>", lambda event: validate())

    # Attendre que le dialogue soit fermé
    return dialog


def remove_node_dialog(parent, on_validate, nodes_list):
    """Crée un dialogue pour supprimer un nœud"""
    if not nodes_list:
        messagebox.showinfo("Information", "Le graphe est vide.")
        return None

    dialog, frame = create_dialog(parent, "Supprimer un sommet", 400, 220)

    # Label
    ttk.Label(frame, text="Choisissez le sommet à supprimer:",
              font=('Arial', 16), style='Dialog.TLabel').pack(pady=(0, 15))

    # Liste déroulante des sommets
    node_var = tk.StringVar()
    combo = ttk.Combobox(frame, textvariable=node_var, values=nodes_list,
                         font=('Arial', 16), width=20, state="readonly")
    combo.pack(pady=(0, 25))
    if nodes_list:
        combo.current(0)
    combo.focus_set()

    # Fonction de validation
    def validate():
        node = node_var.get()
        if node:
            on_validate(node)
            dialog.destroy()

    # Boutons
    btn_frame = ttk.Frame(frame)
    btn_frame.pack(fill=tk.X)

    cancel_btn = ttk.Button(btn_frame, text="Annuler", command=dialog.destroy, width=12)
    cancel_btn.pack(side=tk.LEFT, padx=10)

    delete_btn = ttk.Button(btn_frame, text="Supprimer", command=validate,
                            style='Delete.TButton', width=12)
    delete_btn.pack(side=tk.RIGHT, padx=10)

    return dialog


def add_edge_dialog(parent, on_validate, nodes_list):
    """Crée un dialogue pour ajouter un arc"""
    if len(nodes_list) < 2:
        messagebox.showinfo("Information", "Ajoutez au moins deux sommets d'abord.")
        return None

    dialog, frame = create_dialog(parent, "Ajouter un arc", 500, 320)

    # Variables pour stocker les valeurs
    source_var = tk.StringVar()
    target_var = tk.StringVar()
    weight_var = tk.DoubleVar(value=1.0)

    # Labels et champs
    ttk.Label(frame, text="Sommet de départ:", font=('Arial', 16)).grid(row=0, column=0, sticky='w', pady=(0, 10))
    source_combo = ttk.Combobox(frame, textvariable=source_var, values=nodes_list,
                                font=('Arial', 16), width=20, state="readonly")
    source_combo.grid(row=0, column=1, sticky='w', pady=(0, 20))
    source_combo.current(0)  # Sélectionner le premier sommet par défaut

    ttk.Label(frame, text="Sommet d'arrivée:", font=('Arial', 16)).grid(row=1, column=0, sticky='w', pady=(0, 10))
    target_combo = ttk.Combobox(frame, textvariable=target_var, values=nodes_list,
                                font=('Arial', 16), width=20, state="readonly")
    target_combo.grid(row=1, column=1, sticky='w', pady=(0, 20))
    if len(nodes_list) > 1:
        target_combo.current(1)  # Sélectionner le deuxième sommet par défaut

    ttk.Label(frame, text="Poids de l'arc:", font=('Arial', 16)).grid(row=2, column=0, sticky='w', pady=(0, 10))
    weight_spinbox = ttk.Spinbox(frame, from_=0.1, to=100, increment=0.1,
                                 textvariable=weight_var, font=('Arial', 16), width=10)
    weight_spinbox.grid(row=2, column=1, sticky='w', pady=(0, 25))

    # Message d'état
    status_var = tk.StringVar()
    status_label = ttk.Label(frame, textvariable=status_var,
                             font=('Arial', 14), foreground='red')
    status_label.grid(row=3, column=0, columnspan=2, sticky='w', pady=(0, 15))

    # Fonction de validation
    def validate():
        source = source_var.get()
        target = target_var.get()

        if source == target:
            status_var.set("Erreur: Les sommets de départ et d'arrivée doivent être différents.")
            return

        try:
            weight = weight_var.get()
            if weight <= 0:
                status_var.set("Erreur: Le poids doit être positif.")
                return

            on_validate(source, target, weight)
            dialog.destroy()
        except Exception as e:
            status_var.set(f"Erreur: {str(e)}")

    # Boutons
    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=4, column=0, columnspan=2, pady=(15, 0))

    cancel_btn = ttk.Button(btn_frame, text="Annuler", command=dialog.destroy, width=12)
    cancel_btn.pack(side=tk.LEFT, padx=15)

    add_btn = ttk.Button(btn_frame, text="Ajouter", command=validate,
                         style='Accent.TButton', width=12)
    add_btn.pack(side=tk.RIGHT, padx=15)

    return dialog


def find_path_dialog(parent, on_validate, nodes_list):
    """Crée un dialogue pour rechercher un chemin"""
    dialog, frame = create_dialog(parent, "Rechercher un chemin", 500, 250)

    # Variables pour stocker les valeurs
    source_var = tk.StringVar()
    target_var = tk.StringVar()

    # Labels et champs
    ttk.Label(frame, text="Sommet de départ:", font=('Arial', 16)).grid(row=0, column=0, sticky='w', pady=(0, 10))
    source_combo = ttk.Combobox(frame, textvariable=source_var, values=nodes_list,
                                font=('Arial', 16), width=20, state="readonly")
    source_combo.grid(row=0, column=1, sticky='w', pady=(0, 20))
    source_combo.current(0)  # Sélectionner le premier sommet par défaut

    ttk.Label(frame, text="Sommet d'arrivée:", font=('Arial', 16)).grid(row=1, column=0, sticky='w', pady=(0, 10))
    target_combo = ttk.Combobox(frame, textvariable=target_var, values=nodes_list,
                                font=('Arial', 16), width=20, state="readonly")
    target_combo.grid(row=1, column=1, sticky='w', pady=(0, 20))
    if len(nodes_list) > 1:
        target_combo.current(len(nodes_list) - 1)  # Sélectionner le dernier sommet par défaut

    # Message d'état
    status_var = tk.StringVar()
    status_label = ttk.Label(frame, textvariable=status_var,
                             font=('Arial', 14), foreground='red')
    status_label.grid(row=2, column=0, columnspan=2, sticky='w', pady=(0, 15))

    # Fonction de validation
    def validate():
        source = source_var.get()
        target = target_var.get()

        if source and target:
            result = on_validate(source, target)
            if not result:
                status_var.set(f"Il n'existe pas de chemin de '{source}' à '{target}'.")
            else:
                dialog.destroy()

    # Boutons
    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=3, column=0, columnspan=2, pady=(15, 0))

    cancel_btn = ttk.Button(btn_frame, text="Annuler", command=dialog.destroy, width=12)
    cancel_btn.pack(side=tk.LEFT, padx=15)

    search_btn = ttk.Button(btn_frame, text="Rechercher", command=validate,
                            style='Accent.TButton', width=12)
    search_btn.pack(side=tk.RIGHT, padx=15)

    return dialog