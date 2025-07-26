# main.py

import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk  # Import pour gérer les images
from stegano.embedder import embed_data
from stegano.extractor import extract_data
from stegano.crypto_utils import encrypt, decrypt
from stegano.image_utils import image_to_bytes, bytes_to_image, save_image


class SteganoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("App de Stéganographie")
        self.root.geometry("600x550")

        self.cover_image_path = None
        self.secret_image_path = None
        self.password = ""

        self.init_ui()

    def init_ui(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Ajouter le logo au sommet
        self.add_logo()

        # Sélection d'images
        self.cover_btn = ctk.CTkButton(self.root, text="Choisir image de couverture", command=self.select_cover)
        self.cover_btn.pack(pady=10)

        self.secret_btn = ctk.CTkButton(self.root, text="Choisir image secrète", command=self.select_secret)
        self.secret_btn.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self.root, placeholder_text="Mot de passe")
        self.password_entry.pack(pady=10)

        self.progress = ctk.CTkProgressBar(self.root)
        self.progress.pack(pady=10)
        self.progress.set(0)

        self.embed_btn = ctk.CTkButton(self.root, text="Cacher l'image", command=self.embed_image)
        self.embed_btn.pack(pady=10)

        self.extract_btn = ctk.CTkButton(self.root, text="Extraire l'image", command=self.extract_image)
        self.extract_btn.pack(pady=10)

        self.feedback = ctk.CTkLabel(self.root, text="")
        self.feedback.pack(pady=10)

        # Section information
        self.info_label = ctk.CTkLabel(self.root,
                                       text="Comment utiliser :\n"
                                            "- Choisissez l'image de couverture.\n"
                                            "- Choisissez l'image secrète à cacher.\n"
                                            "- Entrez un mot de passe.\n"
                                            "- Cliquez sur 'Cacher l'image' pour cacher.\n"
                                            "- Pour extraire, sélectionnez l'image de couverture, entrez le mot de passe, et cliquez sur 'Extraire l'image'.",
                                       font=("Arial", 10),  # Police et taille
                                       justify="left")  # Alignement à gauche
        self.info_label.pack(pady=10)

    def add_logo(self):
        try:
            # Charger l'image avec PIL
            logo_image = Image.open("logo.png")
            # Redimensionner l'image si nécessaire (par exemple 100x100)
            #logo_image = logo_image.resize((100, 100), Image.ANTIALIAS)
            # Convertir en CTkImage pour compatibilité avec CustomTkinter
            self.logo_photo = ctk.CTkImage(light_image=logo_image, size=(100, 100))

            # Créer un label pour afficher le logo
            self.logo_label = ctk.CTkLabel(self.root, image=self.logo_photo)
            self.logo_label.pack(pady=10)
        except Exception as e:
            print(f"Erreur lors du chargement du logo : {e}")


    def select_cover(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.bmp")])
        if path:
            self.cover_image_path = path
            self.feedback.configure(text="Image de couverture chargée")

    def select_secret(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.bmp")])
        if path:
            self.secret_image_path = path
            self.feedback.configure(text="Image secrète chargée")

    def embed_image(self):
        self.progress.set(0.2)
        self.password = self.password_entry.get()
        if not self.cover_image_path or not self.secret_image_path or not self.password:
            self.feedback.configure(text="Veuillez choisir deux images et un mot de passe.")
            return

        try:
            secret_bytes = image_to_bytes(self.secret_image_path)
            encrypted_data = encrypt(secret_bytes, self.password)
            embed_data(self.cover_image_path, encrypted_data, "stego_image.png")
            self.progress.set(1)
            self.feedback.configure(text="✅ Image cachée avec succès ! Fichier : stego_image.png")
        except Exception as e:
            self.feedback.configure(text=f"❌ Erreur: {str(e)}")

    def extract_image(self):
        self.progress.set(0.2)
        self.password = self.password_entry.get()
        if not self.cover_image_path or not self.password:
            self.feedback.configure(text="Veuillez choisir une image de couverture et un mot de passe.")
            return

        try:
            encrypted_data = extract_data(self.cover_image_path)
            decrypted_bytes = decrypt(encrypted_data, self.password)
            image = bytes_to_image(decrypted_bytes)
            save_image(image, "extracted_secret.png")
            self.progress.set(1)
            self.feedback.configure(text="✅ Image extraite avec succès ! Fichier : extracted_secret.png")
        except ValueError:
            self.password_entry.delete(0, 'end')
            self.progress.set(0)
            self.feedback.configure(text="❌ Mot de passe incorrect.")
        except Exception as e:
            self.feedback.configure(text=f"❌ Erreur: {str(e)}")


if __name__ == "__main__":
    root = ctk.CTk()
    app = SteganoApp(root)
    root.mainloop()
