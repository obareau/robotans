import tkinter as tk
from itertools import groupby

# Dictionnaire pour associer une lettre à une note de musique avec octaves
def letter_to_note_with_octave(letter):
    """Convertit une lettre en note de musique avec octaves."""
    notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    letter = letter.upper()
    if letter.isalpha():
        index = ord(letter) - ord('A')  # Index de 0 à 25 pour A-Z
        note = notes[index % 7]  # Sélectionne la note (A à G)
        octave = (index // 7) + 1  # Calcule l'octave
        return f"{note}{octave}"
    return letter  # Conserve les autres caractères tels quels

def cesar_cipher(text, shift=3):
    """Applique un décalage César de `shift` sur le texte donné."""
    result = []
    for char in text.upper():
        if char.isalpha():
            shifted_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
            result.append(shifted_char)
        elif char.isdigit():
            result.append(char)  # Conserve les chiffres
    return "".join(result)

def group_by_five(text):
    """Groupe les lettres du texte par blocs de 5."""
    grouped = " ".join(text[i:i+5] for i in range(0, len(text), 5))
    return grouped

def reverse_text(text):
    """Inverse l'ordre des caractères dans le texte."""
    return text[::-1]

def letter_to_music_with_octave(text):
    """Convertit chaque lettre en note de musique avec octaves."""
    return " ".join(letter_to_note_with_octave(char) for char in text if char.isalpha())

def group_words_by_four(text):
    """Groupe les mots par blocs de 4 avec formatage."""
    words = text.split()
    grouped_blocks = [
        " ".join(words[i:i+4]).capitalize()
        for i in range(0, len(words), 4)
    ]
    return " / ".join(grouped_blocks)

def flash_order(text):
    """Convertit le texte en format 'Ordre Flash'."""
    # Supprimer les espaces
    text = text.replace(" ", "")
    # Factoriser les lettres consécutives
    factorized = "".join(
        f"{char}{len(list(group)) if len(list(group)) > 1 else ''}"
        for char, group in groupby(text)
    )
    # Encadrer avec "!"
    return f"!{factorized}!"

def convert_to_robotan_language_v1(text):
    """Convertit le texte en langage de bataille Robotans V1."""
    ciphered_text = cesar_cipher(text)
    grouped_text = group_by_five(ciphered_text)
    return grouped_text

def convert_to_robotan_language_v2(text):
    """Convertit le texte en langage de bataille Robotans V2 (cryptage renforcé)."""
    ciphered_text = cesar_cipher(text)
    reversed_text = reverse_text(ciphered_text)
    grouped_text = group_by_five(reversed_text)
    return grouped_text

def convert_to_robotan_language_v3(text):
    """Convertit le texte en langage de bataille Robotans V3 (notes de musique avec octaves)."""
    music_text = letter_to_music_with_octave(text)
    grouped_text = group_words_by_four(music_text)
    return grouped_text

class RobotanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Langage de Bataille Robotans")

        # Interface graphique
        self.label_input = tk.Label(root, text="Entrez le texte :", font=("Helvetica", 12))
        self.label_input.pack(pady=10)

        self.text_input = tk.Entry(root, width=50, font=("Helvetica", 12))
        self.text_input.pack(pady=10)

        self.convert_button_v1 = tk.Button(root, text="Convertir (Robotans V1)", font=("Helvetica", 12), command=self.convert_text_v1)
        self.convert_button_v1.pack(pady=5)

        self.convert_button_v2 = tk.Button(root, text="Convertir (Robotans V2)", font=("Helvetica", 12), command=self.convert_text_v2)
        self.convert_button_v2.pack(pady=5)

        self.convert_button_v3 = tk.Button(root, text="Convertir (Robotans V3)", font=("Helvetica", 12), command=self.convert_text_v3)
        self.convert_button_v3.pack(pady=5)

        self.convert_button_flash = tk.Button(root, text="Convertir (Ordre Flash)", font=("Helvetica", 12), command=self.convert_text_flash)
        self.convert_button_flash.pack(pady=5)

        self.label_output = tk.Label(root, text="Texte converti :", font=("Helvetica", 12))
        self.label_output.pack(pady=10)

        self.text_output = tk.Text(root, height=5, width=50, font=("Helvetica", 12), state=tk.DISABLED)
        self.text_output.pack(pady=10)

    def convert_text_v1(self):
        """Convertit le texte entré en langage de bataille Robotans V1."""
        input_text = self.text_input.get()
        converted_text = convert_to_robotan_language_v1(input_text)
        self.display_output(converted_text)

    def convert_text_v2(self):
        """Convertit le texte entré en langage de bataille Robotans V2."""
        input_text = self.text_input.get()
        converted_text = convert_to_robotan_language_v2(input_text)
        self.display_output(converted_text)

    def convert_text_v3(self):
        """Convertit le texte entré en langage de bataille Robotans V3."""
        input_text = self.text_input.get()
        converted_text = convert_to_robotan_language_v3(input_text)
        self.display_output(converted_text)

    def convert_text_flash(self):
        """Convertit le texte entré en format 'Ordre Flash'."""
        input_text = self.text_input.get()
        converted_text = flash_order(input_text)
        self.display_output(converted_text)

    def display_output(self, text):
        """Affiche le texte converti dans le panneau de sortie."""
        self.text_output.config(state=tk.NORMAL)
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert(tk.END, text)
        self.text_output.config(state=tk.DISABLED)

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = RobotanApp(root)
    root.mainloop()
