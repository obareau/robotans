import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# Données de base
start_date = datetime(1972, 1, 1)  # 1er Ordium, An 0 de la Rectitude
months = [
    "Ordium", "Fervor", "Laboris", "Prudium", "Valoris",
    "Constium", "Septium", "Servium", "Fortium", "Decorum",
    "Rectium", "Finalis", "Jours du Silence"
]

ceremonies = {
    # Cérémonies et événements récurrents
    "15 Ordium": "Cérémonie de la Fondation",
    "25 Fervor": "Rite de la Fraternité",
    "5 Laboris": "Cérémonie des Mains du Travail",
    "10 Laboris": "Rituel de la Diligence",
    "15 Prudium": "Rituel de la Vigilance",
    "18 Valoris": "Honneur aux Méritants",
    "28 Constium": "Serment de l’Éternelle Fidélité",
    "5 Septium": "Marche de la Dévotion",
    "14 Septium": "Jour de la Perfection",
    "15 Septium": "Anniversaire du Premier Prototype Homo Mecanicus",
    "18 Servium": "Fête du Service",
    "20 Fortium": "Fête de la Résilience",
    "12 Fortium": "Épreuves de Résilience",
    "10 Decorum": "Semaine de la Rectitude",
    "15 Decorum": "Rites de la Perfection Esthétique",
    "30 Decorum": "Cérémonie du Serment de Pureté",
    "10 Rectium": "Cérémonie des Légataires",
    "15 Rectium": "Apparition des enfants hybrides",
    "20 Finalis": "Rite de la Purification",
    "25 Finalis": "Veillée de la Pureté",
    "30 Finalis": "La Veillée du Recueillement",

    # Jours du Silence
    "1 Jours du Silence": "L'Apurement",
    "2 Jours du Silence": "Les Jours de la Conformité",
    "3 Jours du Silence": "La Récitation de la Rectitude",
    "4 Jours du Silence": "Le Jour du Réveil",
    "5 Jours du Silence": "Le Grand Appurement (année bissextile uniquement)",

    # Dates spéciales (100e, 200e, 300e jours)
    "10 Laboris": "100e jour de l'année",
    "20 Fortium": "200e jour de l'année",
    "30 Decorum": "300e jour de l'année",

    # Dates historiques
    "1 Ordium, An 0": "Création officielle de la Rectitude (1er janvier 1972)",
    "8 Fervor, An 20": "Commémoration de la Première Rébellion Contrôlée (8 février 1992)",
    "15 Septium, An 42": "Premier prototype Homo Mecanicus (15 juillet 2014)",
    "15 Rectium, An 45": "Naissance des enfants hybrides (15 novembre 2017)"
}


special_dates = {
    "10 Laboris": "100e jour de l'année",
    "20 Fortium": "200e jour de l'année",
    "30 Decorum": "300e jour de l'année",
}

# Fusion des cérémonies et des dates spéciales
ceremonies.update(special_dates)

# Conversion des dates de la Rectitude en date réelle
def get_real_date(an, mois, jour):
    """Convertir une date de la Rectitude en date réelle."""
    rectitude_start = start_date
    days_since_start = (an * 360) + ((mois - 1) * 30) + jour - 1
    return rectitude_start + timedelta(days=days_since_start)

def is_leap_year(year):
    """Déterminer si une année est bissextile."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendrier de la Rectitude")

        # Variables
        self.current_month_index = 0
        self.current_year = 0
        self.custom_events = {}

        # Widgets principaux
        self.header_frame = tk.Frame(root)
        self.header_frame.pack()

        self.calendar_frame = tk.Frame(root)
        self.calendar_frame.pack()

        self.ceremony_frame = tk.Frame(root, bg="lightgrey")
        self.ceremony_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Boutons pour navigation
        self.year_label = tk.Label(self.header_frame, text=f"Année : {self.current_year}", font=("Helvetica", 16, "bold"))
        self.year_label.pack(side=tk.LEFT, padx=10)

        prev_button = tk.Button(self.header_frame, text="<< Mois Précédent", command=self.prev_month)
        prev_button.pack(side=tk.LEFT)

        next_button = tk.Button(self.header_frame, text="Mois Suivant >>", command=self.next_month)
        next_button.pack(side=tk.RIGHT)

        add_event_button = tk.Button(self.header_frame, text="Ajouter un événement", command=self.add_event)
        add_event_button.pack(side=tk.RIGHT, padx=10)

        manage_event_button = tk.Button(self.header_frame, text="Gérer les événements", command=self.manage_event)
        manage_event_button.pack(side=tk.RIGHT, padx=10)

        self.month_label = tk.Label(root, text=months[self.current_month_index], font=("Helvetica", 18, "bold"))
        self.month_label.pack(pady=10)



        # Affichage initial
        self.show_calendar()
        self.show_ceremonies()

    def get_days_in_month(self):
        """Obtenir le nombre de jours dans le mois actuel."""
        if self.current_month_index < 12:
            return 30
        return 5 if is_leap_year(self.current_year + 1972) else 4

    def show_calendar(self):
        """Afficher le calendrier pour le mois actuel."""
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        days_in_month = self.get_days_in_month()
        for day in range(1, days_in_month + 1):
            day_str = f"{day} {months[self.current_month_index]}"
            ceremony = ceremonies.get(day_str, "")
            custom_event = self.custom_events.get(day_str, "")

            # Création d'une cellule de jour
            day_label = tk.Label(self.calendar_frame, text=f"{day:02d}", width=4, font=("Helvetica", 14))
            day_label.grid(row=(day - 1) // 7, column=(day - 1) % 7, padx=5, pady=5)

            if ceremony or custom_event:
                day_label.config(bg="yellow", relief="solid")

    def show_ceremonies(self):
        """Afficher les cérémonies dans un panneau séparé."""
        for widget in self.ceremony_frame.winfo_children():
            widget.destroy()

        tk.Label(self.ceremony_frame, text="Cérémonies et Événements :",
                 font=("Helvetica", 14, "bold"), bg="lightgrey").pack(anchor="w", padx=10, pady=5)

        days_in_month = self.get_days_in_month()
        for day in range(1, days_in_month + 1):
            day_str = f"{day} {months[self.current_month_index]}"
            ceremony = ceremonies.get(day_str, "")
            custom_event = self.custom_events.get(day_str, "")

            if ceremony or custom_event:
                event_text = f"{day:02d} : {ceremony}" if ceremony else f"{day:02d} : {custom_event}"
                tk.Label(self.ceremony_frame, text=event_text, bg="lightgrey", font=("Helvetica", 12)).pack(anchor="w", padx=10)

    def prev_month(self):
        """Afficher le mois précédent."""
        if self.current_month_index > 0:
            self.current_month_index -= 1
        else:
            self.current_month_index = len(months) - 1
            self.current_year -= 1
            self.year_label.config(text=f"Année : {self.current_year}")
        self.month_label.config(text=months[self.current_month_index])
        self.show_calendar()
        self.show_ceremonies()

    def next_month(self):
        """Afficher le mois suivant."""
        if self.current_month_index < len(months) - 1:
            self.current_month_index += 1
        else:
            self.current_month_index = 0
            self.current_year += 1
            self.year_label.config(text=f"Année : {self.current_year}")
        self.month_label.config(text=months[self.current_month_index])
        self.show_calendar()
        self.show_ceremonies()

    def add_event(self):
        """Ajouter un événement personnalisé."""
        def save_event():
            day = int(day_var.get())
            event = event_entry.get()
            month = months[self.current_month_index]
            self.custom_events[f"{day} {month}"] = event
            add_event_window.destroy()
            self.show_calendar()
            self.show_ceremonies()

        add_event_window = tk.Toplevel(self.root)
        add_event_window.title("Ajouter un événement")

        tk.Label(add_event_window, text="Jour :").grid(row=0, column=0, padx=10, pady=10)
        day_var = tk.StringVar(value="1")
        tk.Entry(add_event_window, textvariable=day_var).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(add_event_window, text="Événement :").grid(row=1, column=0, padx=10, pady=10)
        event_entry = tk.Entry(add_event_window)
        event_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(add_event_window, text="Sauvegarder", command=save_event).grid(row=2, column=0, columnspan=2, pady=10)

    def manage_event(self):
        """Gérer les événements existants."""
        def delete_event():
            selected_event = event_listbox.get(tk.ACTIVE)
            if selected_event:
                day_str = selected_event.split(":")[0].strip()
                if day_str in self.custom_events:
                    del self.custom_events[day_str]
                    del self.custom_events[day_str]
                    self.show_calendar()
                    self.show_ceremonies()
            manage_event_window.destroy()

        def edit_event():
            selected_event = event_listbox.get(tk.ACTIVE)
            if selected_event:
                day_str = selected_event.split(":")[0].strip()
                if day_str in self.custom_events:
                    new_event_text = event_entry.get()
                    self.custom_events[day_str] = new_event_text
                    self.show_calendar()
                    self.show_ceremonies()
            manage_event_window.destroy()

        manage_event_window = tk.Toplevel(self.root)
        manage_event_window.title("Gérer les événements")

        tk.Label(manage_event_window, text="Événements actuels :").pack(pady=10)
        event_listbox = tk.Listbox(manage_event_window, width=40, height=10)
        event_listbox.pack(pady=10)

        # Ajouter les événements existants dans la liste
        for day_str, event in self.custom_events.items():
            event_listbox.insert(tk.END, f"{day_str} : {event}")

        tk.Label(manage_event_window, text="Modifier l'événement sélectionné :").pack(pady=10)
        event_entry = tk.Entry(manage_event_window)
        event_entry.pack(pady=10)

        tk.Button(manage_event_window, text="Modifier", command=edit_event).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(manage_event_window, text="Supprimer", command=delete_event).pack(side=tk.RIGHT, padx=10, pady=10)

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()

