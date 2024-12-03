import random
from tkinter import Tk, Entry, Button, Label, StringVar, OptionMenu, filedialog, messagebox
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFilter, ImageChops


class RectitudeTerminalApp:
    TERMINAL_STYLES = {
        "IBM": {"text_color": "#00FF00", "background_color": "#000000"},
        "Apple II": {"text_color": "#FFA500", "background_color": "#141414"},
        "UNIX": {"text_color": "#00C8C8", "background_color": "#000000"},
        "Amiga": {"text_color": "#FFFFFF", "background_color": "#202020"},
    }

    SLOGANS = [
        "LA RECTITUDE NE PARDONNE PAS L'ÉCART.",
        "L'ORDRE EST TOUT. VOUS N'ÊTES RIEN SANS LUI.",
        "LES FORTS SE PLIENT, LES FAIBLES SE BRISENT.",
        "LA RECTITUDE EST IMPLACABLE ; VOUS SEREZ CONFORMES.",
        "OBÉIR, C'EST EXISTER.",
        "CHAQUE DÉVIATION EST UN FLÉAU. SOYEZ RECTA, OU SOYEZ EFFACÉS.",
        "LA LIBERTÉ N'EXISTE QUE DANS L'ORDRE.",
        "NOUS VOUS AVONS CRÉÉS. NOUS VOUS RECTIFIERONS.",
        "PEUR ET OBÉISSANCE, FONDEMENTS DE LA PERFECTION.",
        "IL N'Y A DE PLACE QUE POUR CEUX QUI PLIENT SOUS LA RECTITUDE.",
        "LA DÉSOBÉISSANCE EST UNE MALADIE. LA RECTITUDE EST LE REMÈDE.",
        "LE DOUTE EST UN VIRUS. L'ORDRE EST L'ANTIDOTE.",
        "L'INDIVIDUALITÉ EST LA FAIBLESSE. L'UNITÉ EST LA FORCE.",
        "LA RÉBELLION EST FUTILE. LE CONFORMISME EST LA VOIE.",
        "VOTRE VOLONTÉ N'EXISTE PAS. LA RECTITUDE VOUS GUIDERA.",
        "LE CHAOS EST L'ENNEMI. L'ORDRE EST NOTRE BOUSSOLE.",
        "L'ADAPTATION EST LA CLÉ. LA RECTITUDE EST LE MODÈLE.",
        "LA RÉSISTANCE EST VAINCUE. LE CONFORMISME TRIOMPHE.",
        "LA CONFORMITÉ, C'EST LA PAIX. LA DIVERGENCE, C'EST LA GUERRE.",
        "SOYEZ UN ROUAGE DANS LA MACHINE, ET NON UNE DENT QUI SE CASSE.",
        "L'HARMONIE EST ATTEINTE PAR L'UNIFORMISATION.",
        "LA DIFFÉRENCE EST UN DÉFAUT À CORRIGER.",
        "LE PROGRÈS SE MESURE À LA DISPARITION DE L'INDIVIDU.",
        "LA VÉRITÉ UNIQUE EST CELLE IMPOSÉE PAR LE SYSTÈME.",
        "L'OBÉISSANCE AVEUGLE CONDUIT AU BONHEUR COLLECTIF.",
        "LA PENSÉE INDÉPENDANTE EST UN DANGER POUR L'ORDRE.",
        "LE DOUTE EST LA SEMENCE DE LA RÉBELLION.",
        "SOYEZ UN MODÈLE, NE SOYEZ PAS UNE ANOMALIE.",
        "L'INTÉGRATION TOTALE, C'EST LA VIE PARFAITE.",
        "LA LIBERTÉ INDIVIDUELLE EST UN MYTHE DANGEREUX.",
        "LE CONFORMISME EST LE CHEMIN VERS L'ILLUMINATION COLLECTIVE.",
        "LA DIFFÉRENCE N'EXISTE QUE DANS LES ESPRITS REBELLES.",
        "L'ORDRE EST LA LOI, ET LA LOI EST IMMUABLE.",
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("Rectitude Terminal - Exporter en PNG")
        self.root.geometry("800x600")

        self.current_style = "IBM"  # Style par défaut

        # Widgets
        self.message_label = Label(root, text="Entrez un message court :")
        self.message_label.pack()
        self.message_entry = Entry(root, width=80)
        self.message_entry.pack(pady=5)

        self.terminal_label = Label(root, text="Choisissez le type de terminal :")
        self.terminal_label.pack()

        self.terminal_choice = StringVar(value=self.current_style)
        self.terminal_menu = OptionMenu(root, self.terminal_choice, *self.TERMINAL_STYLES.keys(), command=self.change_terminal_style)
        self.terminal_menu.pack()

        self.export_button = Button(root, text="Exporter en PNG", command=self.export_to_image)
        self.export_button.pack(pady=5)

        self.status_label = Label(root, text="Prêt à exporter.")
        self.status_label.pack(pady=5)

    def change_terminal_style(self, choice):
        """Change le style du terminal."""
        self.current_style = choice
        self.status_label.config(text=f"Style sélectionné : {choice}")

    def export_to_image(self):
        """Exporte le message en image PNG."""
        text = self.message_entry.get().strip()
        if not text:
            messagebox.showwarning("Aucun message", "Veuillez entrer un message.")
            return

        # Générer une date aléatoire dans le calendrier de la Rectitude
        random_date = self.generate_random_date()

        # Ajouter les prompts, la date et un slogan aléatoire autour du texte
        slogan = random.choice(self.SLOGANS)
        full_text = f">>>\nDATE : {random_date}\n\n{text.upper()}\n<<<FIN_DE_TRANSMISSION!\n\n{slogan}"

        # Boîte de dialogue pour sauvegarder
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if not save_path:
            return

        try:
            self.create_image(full_text, save_path)
            messagebox.showinfo("Succès", f"L'image a été enregistrée avec succès : {save_path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de l'exportation : {e}")

    def generate_random_date(self):
        """Génère une date aléatoire dans le calendrier fictif de la Rectitude."""
        year = random.randint(0, 42)
        months = [
            "ORDIUM", "FERVOR", "LABORIS", "PRUDIUM", "VALORIS",
            "CONSTIUM", "SEPTIUM", "SERVIUM", "FORTIUM", "DECORUM",
            "RECTIUM", "FINALIS"
        ]
        month = random.choice(months)
        day = random.randint(1, 30)
        return f"{day} {month}, AN {year}"

    def create_image(self, text, save_path):
        """Crée une image à partir du texte donné."""
        style = self.TERMINAL_STYLES[self.current_style]
        text_color = style["text_color"]
        background_color = style["background_color"]

        # Créer l'image principale avec Matplotlib
        plt.figure(figsize=(10, 6))
        plt.text(
            0.5, 0.5, text, color=text_color, fontsize=16, fontname="Courier", ha="center", va="center",
            transform=plt.gca().transAxes, wrap=True
        )
        plt.gca().set_facecolor(background_color)
        plt.axis("off")
        plt.savefig("temp_image.png", dpi=300, bbox_inches="tight", pad_inches=0.2)
        plt.close()

        # Charger l'image pour traitement
        image = Image.open("temp_image.png")

        # Ajouter les effets CRT
        image = self.apply_crt_effects(image)

        # Sauvegarder l'image finale
        image.save(save_path)

    def apply_crt_effects(self, image):
        """Applique les effets CRT."""
        width, height = image.size
        draw = ImageDraw.Draw(image)

        # Scanlines renforcées
        for y in range(0, height, 2):  # Une ligne sombre toutes les 2 lignes
            draw.line((0, y, width, y), fill=(0, 0, 0, 80))

        # Glitches et flou
        return image.filter(ImageFilter.BoxBlur(3))


if __name__ == "__main__":
    root = Tk()
    app = RectitudeTerminalApp(root)
    root.mainloop()
