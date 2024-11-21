from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

# Définition des mois du Calendrier de la Rectitude
months = [
    "Ordium", "Fervor", "Laboris", "Prudium", "Valoris",
    "Constium", "Septium", "Servium", "Fortium", "Decorum",
    "Rectium", "Finalis", "Jours du Silence"
]

# Cérémonies importantes
ceremonies = {
    "15 Ordium": "Cérémonie de la Fondation",
    "8 Fervor": "Première Rébellion Contrôlée",
    "15 Septium": "Premier prototype Homo Mecanicus",
    "15 Rectium": "Naissance des enfants hybrides",
    "1 Jours du Silence": "L'Apurement",
    "2 Jours du Silence": "Les Jours de la Conformité",
    "3 Jours du Silence": "La Récitation de la Rectitude",
    "4 Jours du Silence": "Le Jour du Réveil",
    "5 Jours du Silence": "Le Grand Appurement (Année bissextile uniquement)"
}

# Fonction globale pour convertir une date Rectitude en date grégorienne
def rectitude_to_gregorian(year, month, day):
    """
    Convertit une date du Calendrier de la Rectitude en une date grégorienne.
    """
    # Point de départ : 1er janvier 1972
    start_date = datetime(1972, 1, 1)
    days_since_start = (year * 360) + ((month - 1) * 30) + (day - 1)
    return start_date + timedelta(days=days_since_start)

# Classe principale de l'application
class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendrier de la Rectitude")

        # Variables d'état
        self.current_year = 0  # An 0
        self.current_month_index = 0  # Ordium
        self.custom_events = {}

        # Cadres principaux
        self.header_frame = tk.Frame(root)
        self.header_frame.pack()

        self.calendar_frame = tk.Frame(root)
        self.calendar_frame.pack()

        self.ceremony_frame = tk.Frame(root, bg="lightgrey")
        self.ceremony_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Boutons de navigation et fonctionnalités
        self.year_label = tk.Label(self.header_frame, text=f"Année : {self.current_year}", font=("Helvetica", 16, "bold"))
        self.year_label.pack(side=tk.LEFT, padx=10)

        prev_button = tk.Button(self.header_frame, text="<< Mois Précédent", command=self.prev_month)
        prev_button.pack(side=tk.LEFT)

        next_button = tk.Button(self.header_frame, text="Mois Suivant >>", command=self.next_month)
        next_button.pack(side=tk.RIGHT)

        self.month_label = tk.Label(root, text=months[self.current_month_index], font=("Helvetica", 18, "bold"))
        self.month_label.pack(pady=10)

        # Afficher le calendrier
        self.show_calendar()
        self.show_ceremonies()

    def get_days_in_month(self):
        """Retourne le nombre de jours dans le mois courant."""
        if self.current_month_index < 12:
            return 30
        return 5 if self.is_leap_year(self.current_year + 1972) else 4

    def is_leap_year(self, year):
        """Vérifie si une année est bissextile."""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def show_calendar(self):
        """Affiche les jours du mois courant dans le calendrier."""
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        days_in_month = self.get_days_in_month()
        for day in range(1, days_in_month + 1):
            day_str = f"{day} {months[self.current_month_index]}"
            ceremony = ceremonies.get(day_str, "")
            day_label = tk.Label(self.calendar_frame, text=f"{day:02d}", width=4, font=("Helvetica", 14))
            day_label.grid(row=(day - 1) // 7, column=(day - 1) % 7, padx=5, pady=5)

            if ceremony:
                day_label.config(bg="yellow", relief="solid")

            # Ajouter le survol pour afficher la date grégorienne
            day_label.bind("<Enter>", lambda e, d=day: self.show_gregorian_date(d))

    def show_gregorian_date(self, day):
        """Affiche une infobulle avec la date grégorienne équivalente."""
        gregorian_date = rectitude_to_gregorian(self.current_year, self.current_month_index + 1, day)
        self.root.title(f"Date sélectionnée : {day} {months[self.current_month_index]}, An {self.current_year} -> {gregorian_date.strftime('%d %B %Y')}")

    def show_ceremonies(self):
        """Affiche les cérémonies dans le panneau des cérémonies."""
        for widget in self.ceremony_frame.winfo_children():
            widget.destroy()

        tk.Label(self.ceremony_frame, text="Cérémonies et événements :", font=("Helvetica", 14, "bold"), bg="lightgrey").pack(anchor="w", padx=10, pady=5)
        days_in_month = self.get_days_in_month()
        for day in range(1, days_in_month + 1):
            day_str = f"{day} {months[self.current_month_index]}"
            ceremony = ceremonies.get(day_str, "")
            if ceremony:
                tk.Label(self.ceremony_frame, text=f"{day:02d} : {ceremony}", bg="lightgrey", font=("Helvetica", 12)).pack(anchor="w", padx=10)

    def prev_month(self):
        """Passe au mois précédent."""
        if self.current_month_index > 0:
            self.current_month_index -= 1
        else:
            self.current_month_index = len(months) - 1
            self.current_year -= 1
        self.update_view()

    def next_month(self):
        """Passe au mois suivant."""
        if self.current_month_index < len(months) - 1:
            self.current_month_index += 1
        else:
            self.current_month_index = 0
            self.current_year += 1
        self.update_view()

    def update_view(self):
        """Met à jour l'affichage de l'année, du mois et des cérémonies."""
        self.year_label.config(text=f"Année : {self.current_year}")
        self.month_label.config(text=months[self.current_month_index])
        self.show_calendar()
        self.show_ceremonies()


# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
