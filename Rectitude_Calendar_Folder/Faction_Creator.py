import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Fichier JSON pour les factions
FACTIONS_FILE = "factions.json"
DEFAULT_FACTIONS = ["Rectitude", "Harmonie Synthétique", "Pureté Humaine"]

def load_factions():
    """Charge les factions depuis le fichier JSON, ou crée un fichier par défaut."""
    if not os.path.exists(FACTIONS_FILE):
        with open(FACTIONS_FILE, "w") as file:
            json.dump(DEFAULT_FACTIONS, file, indent=4)
        return DEFAULT_FACTIONS
    with open(FACTIONS_FILE, "r") as file:
        return json.load(file)

def save_factions(factions):
    """Enregistre les factions dans le fichier JSON."""
    with open(FACTIONS_FILE, "w") as file:
        json.dump(factions, file, indent=4)

class FactionManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Factions")
        
        # Charger les factions
        self.factions = load_factions()

        # Interface graphique
        self.create_widgets()

    def create_widgets(self):
        """Crée les widgets de l'interface."""
        # Liste des factions
        ttk.Label(self.root, text="Factions existantes :").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.faction_listbox = tk.Listbox(self.root, height=15, width=40)
        self.faction_listbox.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.refresh_faction_list()

        # Champs pour ajouter/modifier une faction
        ttk.Label(self.root, text="Nom de la faction :").grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.faction_name_entry = ttk.Entry(self.root, width=30)
        self.faction_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Boutons d'action
        self.add_button = ttk.Button(self.root, text="Ajouter", command=self.add_faction)
        self.add_button.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.update_button = ttk.Button(self.root, text="Modifier", command=self.update_faction)
        self.update_button.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.delete_button = ttk.Button(self.root, text="Supprimer", command=self.delete_faction)
        self.delete_button.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    def refresh_faction_list(self):
        """Recharge la liste des factions affichées."""
        self.faction_listbox.delete(0, tk.END)
        for faction in self.factions:
            self.faction_listbox.insert(tk.END, faction)

    def add_faction(self):
        """Ajoute une nouvelle faction."""
        new_faction = self.faction_name_entry.get().strip()
        if not new_faction:
            messagebox.showwarning("Champ vide", "Le nom de la faction ne peut pas être vide.")
            return
        if new_faction in self.factions:
            messagebox.showwarning("Doublon", "Cette faction existe déjà.")
            return
        self.factions.append(new_faction)
        save_factions(self.factions)
        self.refresh_faction_list()
        self.faction_name_entry.delete(0, tk.END)
        messagebox.showinfo("Succès", f"La faction '{new_faction}' a été ajoutée.")

    def update_faction(self):
        """Modifie une faction existante."""
        selected_index = self.faction_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une faction à modifier.")
            return
        new_name = self.faction_name_entry.get().strip()
        if not new_name:
            messagebox.showwarning("Champ vide", "Le nouveau nom de la faction ne peut pas être vide.")
            return
        selected_faction = self.factions[selected_index[0]]
        if new_name in self.factions and new_name != selected_faction:
            messagebox.showwarning("Doublon", "Une faction portant ce nom existe déjà.")
            return
        self.factions[selected_index[0]] = new_name
        save_factions(self.factions)
        self.refresh_faction_list()
        self.faction_name_entry.delete(0, tk.END)
        messagebox.showinfo("Succès", f"La faction '{selected_faction}' a été modifiée en '{new_name}'.")

    def delete_faction(self):
        """Supprime une faction."""
        selected_index = self.faction_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une faction à supprimer.")
            return
        selected_faction = self.factions.pop(selected_index[0])
        save_factions(self.factions)
        self.refresh_faction_list()
        messagebox.showinfo("Succès", f"La faction '{selected_faction}' a été supprimée.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FactionManagerApp(root)
    root.mainloop()
