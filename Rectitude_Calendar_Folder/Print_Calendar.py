import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Configuration des fichiers
EVENTS_FILE = "events.json"
FACTIONS_FILE = "factions.json"
PERSONS_FILE = "perso.json"
PDF_FILE = "Calendrier_Rectitude_Export.pdf"

# Contenus par défaut
DEFAULT_EVENTS = {
    "Ordium": {
        1: {"name": "Cérémonie de la Réinitialisation", "recurrence": "annuel", "faction": "Rectitude", "person": None},
        15: {"name": "Cérémonie de la Fondation", "recurrence": "annuel", "faction": None, "person": None}
    }
}
DEFAULT_FACTIONS = ["Rectitude", "Harmonie Synthétique", "Pureté Humaine"]
DEFAULT_PERSONS = ["Conseiller en Ordium", "Joy", "Mik-L", "Zoe"]

# Lecture ou création des fichiers JSON
def load_file(filename, default_content):
    """Charge un fichier JSON ou crée un fichier par défaut si nécessaire."""
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            json.dump(default_content, file, indent=4)
        return default_content
    with open(filename, "r") as file:
        return json.load(file)

# Création d'une liste d'événements filtrée
def filter_events(events, factions=None, persons=None, start_month=None, end_month=None):
    """Filtre les événements par faction, personnage, ou plage de dates."""
    filtered = []
    for month, days in events.items():
        if start_month and end_month and not (start_month <= month <= end_month):
            continue
        for day, event in days.items():
            if factions and event.get("faction") not in factions:
                continue
            if persons and event.get("person") not in persons:
                continue
            filtered.append({"month": month, "day": day, **event})
    return filtered

# Exportation d'événements en PDF
def export_events_to_pdf(events, filename):
    """Exporte les événements sélectionnés dans un fichier PDF."""
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Liste des événements exportés", styles["Title"]))
    elements.append(Spacer(1, 20))

    for event in events:
        details = f"{event['month']} {event['day']}: {event['name']} ({event['recurrence']})"
        if event.get("faction"):
            details += f" - Faction : {event['faction']}"
        if event.get("person"):
            details += f" - Personnage : {event['person']}"
        elements.append(Paragraph(details, styles["Normal"]))
        elements.append(Spacer(1, 10))

    doc.build(elements)
    messagebox.showinfo("Exportation réussie", f"Les événements ont été exportés dans {filename}")

# Interface graphique
class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion du Calendrier de la Rectitude")

        # Charger les données
        self.events = load_file(EVENTS_FILE, DEFAULT_EVENTS)
        self.factions = load_file(FACTIONS_FILE, DEFAULT_FACTIONS)
        self.persons = load_file(PERSONS_FILE, DEFAULT_PERSONS)

        # Interface principale
        self.create_widgets()

    def create_widgets(self):
        """Crée les widgets principaux."""
        # Liste des événements
        ttk.Label(self.root, text="Événements existants :").grid(row=0, column=0, padx=10, pady=10)
        self.events_list = tk.Text(self.root, width=60, height=20)
        self.events_list.grid(row=1, column=0, padx=10, pady=10)
        self.refresh_event_list()

        # Liste des factions
        ttk.Label(self.root, text="Factions :").grid(row=0, column=1, padx=10, pady=10)
        self.factions_list = tk.Listbox(self.root, height=10)
        self.factions_list.grid(row=1, column=1, padx=10, pady=10)
        for faction in self.factions:
            self.factions_list.insert(tk.END, faction)

        # Liste des personnages
        ttk.Label(self.root, text="Personnages :").grid(row=0, column=2, padx=10, pady=10)
        self.persons_list = tk.Listbox(self.root, height=10)
        self.persons_list.grid(row=1, column=2, padx=10, pady=10)
        for person in self.persons:
            self.persons_list.insert(tk.END, person)

        # Boutons d'action
        self.export_button = ttk.Button(self.root, text="Exporter en PDF", command=self.export_to_pdf)
        self.export_button.grid(row=2, column=0, padx=10, pady=10)

    def refresh_event_list(self):
        """Affiche les événements dans la liste."""
        self.events_list.delete(1.0, tk.END)
        for month, days in self.events.items():
            self.events_list.insert(tk.END, f"\n{month}:\n")
            for day, event in days.items():
                details = f"  {day}: {event['name']} ({event['recurrence']})"
                if event.get("faction"):
                    details += f" - Faction : {event['faction']}"
                if event.get("person"):
                    details += f" - Personnage : {event['person']}"
                self.events_list.insert(tk.END, details + "\n")

    def export_to_pdf(self):
        """Exporte les événements sélectionnés."""
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not filename:
            return
        export_events_to_pdf(self.events_as_list(), filename)

    def events_as_list(self):
        """Convertit les événements en une liste pour l'export."""
        event_list = []
        for month, days in self.events.items():
            for day, event in days.items():
                event_list.append({"month": month, "day": day, **event})
        return event_list

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
