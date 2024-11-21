import tkinter as tk

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

def convert_to_robotan_language(text):
    """Convertit le texte en langage de bataille Robotans."""
    ciphered_text = cesar_cipher(text)
    grouped_text = group_by_five(ciphered_text)
    return grouped_text

class RobotanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Langage de Bataille Robotans V1")

        # Interface graphique
        self.label_input = tk.Label(root, text="Entrez le texte :", font=("Helvetica", 12))
        self.label_input.pack(pady=10)

        self.text_input = tk.Entry(root, width=50, font=("Helvetica", 12))
        self.text_input.pack(pady=10)

        self.convert_button = tk.Button(root, text="Convertir", font=("Helvetica", 12), command=self.convert_text)
        self.convert_button.pack(pady=10)

        self.label_output = tk.Label(root, text="Texte converti :", font=("Helvetica", 12))
        self.label_output.pack(pady=10)

        self.text_output = tk.Text(root, height=5, width=50, font=("Helvetica", 12), state=tk.DISABLED)
        self.text_output.pack(pady=10)

    def convert_text(self):
        """Convertit le texte entré en langage de bataille Robotans."""
        input_text = self.text_input.get()
        converted_text = convert_to_robotan_language(input_text)
        self.text_output.config(state=tk.NORMAL)
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert(tk.END, converted_text)
        self.text_output.config(state=tk.DISABLED)

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = RobotanApp(root)
    root.mainloop()
