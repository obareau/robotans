import re
import json
import csv
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import ttk
from fpdf import FPDF

# Mois fictifs du calendrier de la Rectitude
RECTITUDE_MONTHS = [
    "Ordium", "Fervor", "Laboris", "Prudium", "Valoris",
    "Constium", "Septium", "Servium", "Fortium",
    "Decorum", "Rectium", "Finalis", "Jours du Silence"
]


class RectitudeCalendar:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendrier de la Rectitude")
        self.events = {}
        self.filepath = None

        # Interface graphique
        self.create_widgets()

    def create_widgets(self):
        """Crée les widgets de l'interface."""
        ttk.Label(self.root, text="Chargement du fichier :").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.load_button = ttk.Button(self.root, text="Charger un fichier", command=self.load_file)
        self.load_button.grid(row=0, column=1, padx=10, pady=10)

        self.save_button = ttk.Button(self.root, text="Sauvegarder les événements", command=self.save_file)
        self.save_button.grid(row=0, column=2, padx=10, pady=10)

        self.export_pdf_button = ttk.Button(self.root, text="Exporter en PDF", command=self.export_to_pdf)
        self.export_pdf_button.grid(row=0, column=3, padx=10, pady=10)

        self.event_display = tk.Text(self.root, width=80, height=30, wrap="word")
        self.event_display.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        self.edit_button = ttk.Button(self.root, text="Modifier un événement", command=self.edit_event)
        self.edit_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    def load_file(self):
        """Charge un fichier (Markdown, CSV ou JSON) et affiche les événements."""
        self.filepath = filedialog.askopenfilename(filetypes=[("Markdown", "*.md"), ("CSV", "*.csv"), ("JSON", "*.json")])
        if not self.filepath:
            return

        try:
            if self.filepath.endswith(".md"):
                with open(self.filepath, "r", encoding="utf-8") as file:
                    content = file.readlines()
                self.parse_markdown(content)
            elif self.filepath.endswith(".csv"):
                with open(self.filepath, "r", encoding="utf-8") as file:
                    reader = csv.reader(file)
                    self.parse_csv(reader)
            elif self.filepath.endswith(".json"):
                with open(self.filepath, "r", encoding="utf-8") as file:
                    data = json.load(file)
                self.parse_json(data)

            self.display_events()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier : {e}")

    def parse_markdown(self, lines):
        """Parse les lignes Markdown pour extraire les événements."""
        self.events = {month: [] for month in RECTITUDE_MONTHS}
        event_pattern = re.compile(r"(\d{1,2})\s+(\w+):\s+(.+)")
        for line in lines:
            match = event_pattern.match(line.strip())
            if match:
                day, month, description = match.groups()
                day = int(day)
                if month in RECTITUDE_MONTHS:
                    self.events[month].append(f"{day}: {description}")

    def parse_csv(self, reader):
        """Parse un fichier CSV pour extraire les événements."""
        self.events = {month: [] for month in RECTITUDE_MONTHS}
        for row in reader:
            if len(row) >= 3:
                day, month, description = row[0], row[1], row[2]
                if month in RECTITUDE_MONTHS:
                    self.events[month].append(f"{day}: {description}")

    def parse_json(self, data):
        """Parse un fichier JSON pour extraire les événements."""
        self.events = {month: [] for month in RECTITUDE_MONTHS}
        for month, events in data.items():
            if month in RECTITUDE_MONTHS:
                for event in events:
                    day, description = event["day"], event["description"]
                    self.events[month].append(f"{day}: {description}")

    def display_events(self):
        """Affiche les événements par mois."""
        self.event_display.delete(1.0, tk.END)
        for month in RECTITUDE_MONTHS:
            self.event_display.insert(tk.END, f"{month}:\n")
            for event in sorted(self.events[month], key=lambda x: int(x.split(":")[0])):
                self.event_display.insert(tk.END, f"  {event}\n")
            self.event_display.insert(tk.END, "\n")

    def save_file(self):
        """Sauvegarde les événements dans le fichier d'origine."""
        if not self.filepath:
            messagebox.showerror("Erreur", "Aucun fichier chargé pour sauvegarde.")
            return

        try:
            if self.filepath.endswith(".md"):
                with open(self.filepath, "w", encoding="utf-8") as file:
                    for month in RECTITUDE_MONTHS:
                        for event in self.events[month]:
                            day, description = event.split(": ")
                            file.write(f"{day} {month}: {description}\n")
            elif self.filepath.endswith(".json"):
                data = {month: [] for month in RECTITUDE_MONTHS}
                for month, events in self.events.items():
                    for event in events:
                        day, description = event.split(": ")
                        data[month].append({"day": int(day), "description": description})
                with open(self.filepath, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4)
            elif self.filepath.endswith(".csv"):
                with open(self.filepath, "w", encoding="utf-8", newline="") as file:
                    writer = csv.writer(file)
                    for month, events in self.events.items():
                        for event in events:
                            day, description = event.split(": ")
                            writer.writerow([day, month, description])
            messagebox.showinfo("Succès", "Les événements ont été sauvegardés avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder le fichier : {e}")

    def export_to_pdf(self):
        """Exporte les événements en PDF."""
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for month in RECTITUDE_MONTHS:
            pdf.set_font("Arial", style="B", size=14)
            pdf.cell(200, 10, txt=month, ln=True)
            pdf.set_font("Arial", size=12)
            for event in sorted(self.events[month], key=lambda x: int(x.split(":")[0])):
                pdf.cell(200, 10, txt=f"  {event}", ln=True)
            pdf.ln(5)

        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_file:
            pdf.output(output_file)
            messagebox.showinfo("Succès", f"PDF exporté avec succès : {output_file}")

    def edit_event(self):
        """Permet de modifier les événements directement dans la zone de texte."""
        messagebox.showinfo("Information", "Modifiez directement les événements dans la zone de texte, puis sauvegardez.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RectitudeCalendar(root)
    root.mainloop()
