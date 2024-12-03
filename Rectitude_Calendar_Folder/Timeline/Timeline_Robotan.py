import plotly.graph_objects as go
import pandas as pd
import re
import os
from tkinter import Tk, Toplevel, Label, Entry, Button, Listbox, StringVar, filedialog, messagebox, END, OptionMenu


class RectitudeCalendar:
    MONTHS = [
        "Ordium", "Fervor", "Laboris", "Prudium",
        "Valoris", "Constium", "Septium", "Servium",
        "Fortium", "Decorum", "Rectium", "Finalis"
    ]

    DAYS_PER_MONTH = 30
    EXTRA_DAYS_NORMAL = 4
    EXTRA_DAYS_LEAP = 5

    @staticmethod
    def is_leap_year(year):
        """Détermine si une année est bissextile."""
        return year % 4 == 0

    @staticmethod
    def date_to_rectitude(year, day_of_year):
        """Convertit un jour de l'année en date du calendrier de la Rectitude."""
        is_leap = RectitudeCalendar.is_leap_year(year)
        days_in_year = len(RectitudeCalendar.MONTHS) * RectitudeCalendar.DAYS_PER_MONTH + (
            RectitudeCalendar.EXTRA_DAYS_LEAP if is_leap else RectitudeCalendar.EXTRA_DAYS_NORMAL
        )

        if day_of_year > days_in_year:
            raise ValueError(f"Jour {day_of_year} hors de l'année {year}.")

        # Calcul du mois et du jour
        for i, month in enumerate(RectitudeCalendar.MONTHS):
            if day_of_year <= RectitudeCalendar.DAYS_PER_MONTH:
                return f"{month} {day_of_year}, AN {year}"
            day_of_year -= RectitudeCalendar.DAYS_PER_MONTH

        # Gestion des jours du silence
        if day_of_year <= RectitudeCalendar.EXTRA_DAYS_NORMAL or (is_leap and day_of_year <= RectitudeCalendar.EXTRA_DAYS_LEAP):
            return f"Jour du Silence {day_of_year - 1}, AN {year}"

        raise ValueError(f"Date invalide pour le jour de l'année {day_of_year}.")


class EventManager:
    CATEGORY_COLORS = {
        "Social": "#1f77b4",  # Bleu
        "Militaire": "#d62728",  # Rouge
        "Technologique": "#2ca02c",  # Vert
        "Émeutes": "#ff7f0e",  # Orange
        "Naissance": "#e377c2",  # Rose
        "Mort": "#7f7f7f",  # Gris
        "Inconnu": "#bcbd22",  # Jaune
    }

    def __init__(self, filepath):
        self.filepath = filepath
        self.events = []
        self.categories = set(self.CATEGORY_COLORS.keys())
        self.load_events()

    def load_events(self):
        """Charge les événements à partir du fichier Markdown."""
        if not os.path.exists(self.filepath):
            return
        with open(self.filepath, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                match = re.match(r"AN (.+) - (.+) \| (.+) \| (.+)", line)
                if match:
                    date, event_name, category, location = match.groups()
                    self.categories.add(category)
                    self.events.append({
                        "Date": date,
                        "Event": event_name,
                        "Category": category,
                        "Location": location
                    })

    def save_events(self):
        """Enregistre les événements dans le fichier Markdown."""
        with open(self.filepath, "w", encoding="utf-8") as file:
            for event in self.events:
                file.write(f"AN {event['Date']} - {event['Event']} | {event['Category']} | {event['Location']}\n")


class TimelineGenerator:
    def __init__(self, events):
        self.events = pd.DataFrame(events)

    def generate_timeline(self):
        """Génère une timeline interactive avec le calendrier de la Rectitude."""
        fig = go.Figure()

        if not self.events.empty:
            # Conversion des dates pour respecter le calendrier de la Rectitude
            self.events["FormattedDate"] = self.events.apply(
                lambda row: self.format_date(row["Date"]), axis=1
            )

            self.events["Color"] = self.events["Category"].apply(
                lambda x: EventManager.CATEGORY_COLORS.get(x, "gray")
            )

            fig.add_trace(
                go.Scatter(
                    x=self.events["FormattedDate"],
                    y=[0] * len(self.events),
                    mode="markers",
                    marker=dict(
                        size=15,
                        color=self.events["Color"],
                    ),
                    text=self.events["Event"] + "<br>Catégorie : " +
                         self.events["Category"] + "<br>Lieu : " +
                         self.events["Location"],
                    hoverinfo="text"
                )
            )

        fig.update_layout(
            title="Timeline des Événements (Calendrier de la Rectitude)",
            xaxis_title="Date",
            yaxis=dict(visible=False),
            showlegend=False,
            hovermode="closest"
        )

        save_path = filedialog.asksaveasfilename(
            title="Enregistrer la timeline interactive",
            defaultextension=".html",
            filetypes=[("HTML Files", "*.html")]
        )
        if save_path:
            fig.write_html(save_path)
            messagebox.showinfo("Succès", f"Timeline sauvegardée : {save_path}")

    def format_date(self, date):
        """Formate une date AN YYYY-MM-DD dans le calendrier de la Rectitude."""
        match = re.match(r"AN (\d+)-(\d+)-(\d+)", date)
        if not match:
            raise ValueError(f"Format de date invalide : {date}")
        year, month, day = map(int, match.groups())

        # Calcul du jour de l'année
        day_of_year = (month - 1) * RectitudeCalendar.DAYS_PER_MONTH + day
        return RectitudeCalendar.date_to_rectitude(year, day_of_year)


class EventEditor:
    def __init__(self, manager):
        self.manager = manager
        self.root = Tk()
        self.root.title("Éditeur d'événements")
        self.init_ui()
        self.update_event_list()
        self.root.mainloop()

    def init_ui(self):
        """Initialise l'interface utilisateur."""
        Label(self.root, text="Événements existants :").pack()
        self.event_listbox = Listbox(self.root, width=80, height=20)
        self.event_listbox.pack()

        Button(self.root, text="Charger un fichier Markdown", command=self.load_file).pack()
        Button(self.root, text="Ajouter un événement", command=self.add_event).pack()
        Button(self.root, text="Modifier l'événement", command=self.edit_event).pack()
        Button(self.root, text="Supprimer l'événement", command=self.delete_event).pack()
        Button(self.root, text="Enregistrer", command=self.save_events).pack()
        Button(self.root, text="Afficher la timeline", command=self.show_timeline).pack()

    def update_event_list(self):
        """Met à jour la liste des événements affichés."""
        self.event_listbox.delete(0, END)
        for event in self.manager.events:
            self.event_listbox.insert(END, f"AN {event['Date']} - {event['Event']} | {event['Category']} | {event['Location']}")

    def load_file(self):
        """Charge un nouveau fichier Markdown."""
        filepath = filedialog.askopenfilename(
            title="Choisissez un fichier Markdown",
            filetypes=[("Markdown Files", "*.md"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filepath:
            self.manager.filepath = filepath
            self.manager.events = []
            self.manager.load_events()
            self.update_event_list()
            messagebox.showinfo("Succès", f"Fichier chargé : {filepath}")

    def add_event(self):
        """Ajoute un nouvel événement."""
        self.open_event_editor()

    def edit_event(self):
        """Modifie l'événement sélectionné."""
        selected = self.event_listbox.curselection()
        if not selected:
            messagebox.showwarning("Attention", "Aucun événement sélectionné.")
            return
        index = selected[0]
        self.open_event_editor(self.manager.events[index], index)

    def delete_event(self):
        """Supprime l'événement sélectionné."""
        selected = self.event_listbox.curselection()
        if not selected:
            messagebox.showwarning("Attention", "Aucun événement sélectionné.")
            return
        index = selected[0]
        del self.manager.events[index]
        self.update_event_list()

    def save_events(self):
        """Enregistre les événements dans le fichier Markdown."""
        self.manager.save_events()
        messagebox.showinfo("Succès", "Événements enregistrés.")

    def open_event_editor(self, event=None, index=None):
        """Ouvre une fenêtre pour ajouter/modifier un événement."""
        editor = Toplevel(self.root)
        editor.title("Ajouter/Modifier un événement")

        date_var = StringVar(value=event["Date"] if event else "")
        event_var = StringVar(value=event["Event"] if event else "")
        category_var = StringVar(value=event["Category"] if event else "")
        location_var = StringVar(value=event["Location"] if event else "")

        Label(editor, text="Date (AN YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
        Entry(editor, textvariable=date_var).grid(row=0, column=1)

        Label(editor, text="Nom de l'événement :").grid(row=1, column=0, sticky="w")
        Entry(editor, textvariable=event_var).grid(row=1, column=1)

        Label(editor, text="Catégorie :").grid(row=2, column=0, sticky="w")
        category_menu = OptionMenu(editor, category_var, *self.manager.categories)
        category_menu.grid(row=2, column=1)

        Label(editor, text="Lieu :").grid(row=3, column=0, sticky="w")
        Entry(editor, textvariable=location_var).grid(row=3, column=1)

        def save_changes():
            new_event = {
                "Date": date_var.get(),
                "Event": event_var.get(),
                "Category": category_var.get(),
                "Location": location_var.get()
            }
            if index is not None:
                self.manager.events[index] = new_event
            else:
                self.manager.events.append(new_event)
            self.update_event_list()
            editor.destroy()

        Button(editor, text="Enregistrer", command=save_changes).grid(row=4, column=0, columnspan=2)

    def show_timeline(self):
        """Affiche la timeline interactive."""
        generator = TimelineGenerator(self.manager.events)
        generator.generate_timeline()


if __name__ == "__main__":
    filepath = "events.md"
    manager = EventManager(filepath)
    EventEditor(manager)
