import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Fichier JSON pour les personnages
PERSONS_FILE = "perso.json"
DEFAULT_PERSONS = ["Conseiller en Ordium", "Joy", "Mik-L", "Zoe"]

def load_persons():
    """Charge les personnages depuis le fichier JSON, ou crée un fichier par défaut."""
    if not os.path.exists(PERSONS_FILE):
        with open(PERSONS_FILE, "w") as file:
            json.dump(DEFAULT_PERSONS, file, indent=4)
        return DEFAULT_PERSONS
    with open(PERSONS_FILE, "r") as file:
        return json.load(file)

def save_persons(persons):
    """Enregistre les personnages dans le fichier JSON."""
    with open(PERSONS_FILE, "w") as file:
        json.dump(persons, file, indent=4)

class PersonManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Personnages")
        
        # Charger les personnages
        self.persons = load_persons()

        # Interface graphique
        self.create_widgets()

    def create_widgets(self):
        """Crée les widgets de l'interface."""
        # Liste des personnages
        ttk.Label(self.root, text="Personnages existants :").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.person_listbox = tk.Listbox(self.root, height=15, width=40)
        self.person_listbox.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.refresh_person_list()

        # Champs pour ajouter/modifier un personnage
        ttk.Label(self.root, text="Nom du personnage :").grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.person_name_entry = ttk.Entry(self.root, width=30)
        self.person_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Boutons d'action
        self.add_button = ttk.Button(self.root, text="Ajouter", command=self.add_person)
        self.add_button.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.update_button = ttk.Button(self.root, text="Modifier", command=self.update_person)
        self.update_button.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.delete_button = ttk.Button(self.root, text="Supprimer", command=self.delete_person)
        self.delete_button.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    def refresh_person_list(self):
        """Recharge la liste des personnages affichés."""
        self.person_listbox.delete(0, tk.END)
        for person in self.persons:
            self.person_listbox.insert(tk.END, person)

    def add_person(self):
        """Ajoute un nouveau personnage."""
        new_person = self.person_name_entry.get().strip()
        if not new_person:
            messagebox.showwarning("Champ vide", "Le nom du personnage ne peut pas être vide.")
            return
        if new_person in self.persons:
            messagebox.showwarning("Doublon", "Ce personnage existe déjà.")
            return
        self.persons.append(new_person)
        save_persons(self.persons)
        self.refresh_person_list()
        self.person_name_entry.delete(0, tk.END)
        messagebox.showinfo("Succès", f"Le personnage '{new_person}' a été ajouté.")

    def update_person(self):
        """Modifie un personnage existant."""
        selected_index = self.person_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un personnage à modifier.")
            return
        new_name = self.person_name_entry.get().strip()
        if not new_name:
            messagebox.showwarning("Champ vide", "Le nouveau nom du personnage ne peut pas être vide.")
            return
        selected_person = self.persons[selected_index[0]]
        if new_name in self.persons and new_name != selected_person:
            messagebox.showwarning("Doublon", "Un personnage portant ce nom existe déjà.")
            return
        self.persons[selected_index[0]] = new_name
        save_persons(self.persons)
        self.refresh_person_list()
        self.person_name_entry.delete(0, tk.END)
        messagebox.showinfo("Succès", f"Le personnage '{selected_person}' a été modifié en '{new_name}'.")

    def delete_person(self):
        """Supprime un personnage."""
        selected_index = self.person_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un personnage à supprimer.")
            return
        selected_person = self.persons.pop(selected_index[0])
        save_persons(self.persons)
        self.refresh_person_list()
        messagebox.showinfo("Succès", f"Le personnage '{selected_person}' a été supprimé.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonManagerApp(root)
    root.mainloop()
