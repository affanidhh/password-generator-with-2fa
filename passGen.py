import random
import string
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
import pyotp
import qrcode
from PIL import Image, ImageTk
import os
import json
import csv
from cryptography.fernet import Fernet

# Génération et gestion des clés de chiffrement
def load_key():
    if not os.path.exists('secret.key'):
        key = Fernet.generate_key()
        with open('secret.key', 'wb') as key_file:
            key_file.write(key)
    else:
        with open('secret.key', 'rb') as key_file:
            key = key_file.read()
    return key

key = load_key()
cipher_suite = Fernet(key)

# Génération de mot de passe
def generate_password(length=12, use_uppercase=True, use_lowercase=True, use_digits=True, use_special=True):
    if not (use_uppercase or use_lowercase or use_digits or use_special):
        raise ValueError("Au moins un type de caractère doit être sélectionné")

    characters = ""
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for i in range(length))

    if use_uppercase and not any(c.isupper() for c in password):
        password = replace_random_char(password, string.ascii_uppercase)
    if use_lowercase and not any(c.islower() for c in password):
        password = replace_random_char(password, string.ascii_lowercase)
    if use_digits and not any(c.isdigit() for c in password):
        password = replace_random_char(password, string.digits)
    if use_special and not any(c in string.punctuation for c in password):
        password = replace_random_char(password, string.punctuation)

    return password

def replace_random_char(password, characters):
    index = random.randint(0, len(password) - 1)
    return password[:index] + random.choice(characters) + password[index + 1:]

# Vérification de la robustesse du mot de passe
def check_password_strength(password):
    length_score = len(password) / 2
    variety_score = sum([any(c in group for c in password) for group in [string.ascii_uppercase, string.ascii_lowercase, string.digits, string.punctuation]]) * 2
    return min(length_score + variety_score, 10)

def on_generate():
    try:
        length = int(entry_length.get())
        use_uppercase = var_uppercase.get()
        use_lowercase = var_lowercase.get()
        use_digits = var_digits.get()
        use_special = var_special.get()
        
        password = generate_password(length, use_uppercase, use_lowercase, use_digits, use_special)
        entry_password.delete(0, tk.END)
        entry_password.insert(0, password)
        root.clipboard_clear()
        root.clipboard_append(password)
        strength = check_password_strength(password)
        label_strength.config(text=f"Robustesse du mot de passe: {strength}/10")
        messagebox.showinfo("Succès", "Mot de passe copié dans le presse-papiers !")
    except ValueError as e:
        messagebox.showerror("Erreur", str(e))

def on_save():
    password = entry_password.get()
    if not password:
        messagebox.showerror("Erreur", "Pas de mot de passe à sauvegarder")
        return
    name = simpledialog.askstring("Sauvegarder mot de passe", "Entrez un nom pour ce mot de passe:")
    if not name:
        return
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()
    with open("passwords.txt", "a") as file:
        file.write(f"{name}: {encrypted_password}\n")
    messagebox.showinfo("Succès", "Mot de passe sauvegardé")

def on_export():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json")])
    if not file_path:
        return
    passwords = []
    with open("passwords.txt", "r") as file:
        for line in file:
            name, encrypted_password = line.strip().split(": ")
            decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
            passwords.append({"name": name, "password": decrypted_password})
    if file_path.endswith(".csv"):
        with open(file_path, "w", newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["name", "password"])
            writer.writeheader()
            writer.writerows(passwords)
    elif file_path.endswith(".json"):
        with open(file_path, "w") as json_file:
            json.dump(passwords, json_file, indent=4)
    messagebox.showinfo("Succès", "Mots de passe exportés")

def on_import():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json")])
    if not file_path:
        return
    passwords = []
    if file_path.endswith(".csv"):
        with open(file_path, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                passwords.append(row)
    elif file_path.endswith(".json"):
        with open(file_path, "r") as json_file:
            passwords = json.load(json_file)
    with open("passwords.txt", "a") as file:
        for password in passwords:
            encrypted_password = cipher_suite.encrypt(password["password"].encode()).decode()
            file.write(f"{password['name']}: {encrypted_password}\n")
    messagebox.showinfo("Succès", "Mots de passe importés")

def setup_2fa():
    global totp
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri("user@example.com", issuer_name="PasswordGeneratorApp")
    
    qr = qrcode.make(uri)
    qr.save("qrcode.png")
    
    qr_image = Image.open("qrcode.png")
    qr_photo = ImageTk.PhotoImage(qr_image)
    
    top = tk.Toplevel()
    top.title("Configurer la double authentification")
    
    label = tk.Label(top, text="Scannez ce QR code avec votre application d'authentification")
    label.pack(pady=10)
    
    qr_label = tk.Label(top, image=qr_photo)
    qr_label.image = qr_photo
    qr_label.pack(pady=10)
    
    verify_button = tk.Button(top, text="Vérifier le code", command=verify_2fa)
    verify_button.pack(pady=10)

def verify_2fa():
    code = simpledialog.askstring("Vérification du code", "Entrez le code à 6 chiffres de votre application d'authentification:")
    if totp.verify(code):
        messagebox.showinfo("Succès", "Code vérifié avec succès.")
    else:
        messagebox.showerror("Erreur", "Code incorrect. Veuillez réessayer.")

# Configuration de l'interface graphique
root = tk.Tk()
root.title("Générateur de mot de passe avec 2FA")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Longueur du mot de passe:").grid(row=0, column=0, sticky="e")
entry_length = tk.Entry(frame)
entry_length.grid(row=0, column=1)
entry_length.insert(0, "12")

var_uppercase = tk.BooleanVar(value=True)
var_lowercase = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=True)

tk.Checkbutton(frame, text="Lettres majuscules", variable=var_uppercase).grid(row=1, columnspan=2, sticky="w")
tk.Checkbutton(frame, text="Lettres minuscules", variable=var_lowercase).grid(row=2, columnspan=2, sticky="w")
tk.Checkbutton(frame, text="Chiffres", variable=var_digits).grid(row=3, columnspan=2, sticky="w")
tk.Checkbutton(frame, text="Caractères spéciaux", variable=var_special).grid(row=4, columnspan=2, sticky="w")

tk.Button(frame, text="Générer", command=on_generate).grid(row=5, columnspan=2)
entry_password = tk.Entry(frame, width=50)
entry_password.grid(row=6, columnspan=2)

label_strength = tk.Label(frame, text="Robustesse du mot de passe: ")
label_strength.grid(row=7, columnspan=2)

tk.Button(frame, text="Configurer 2FA", command=setup_2fa).grid(row=8, columnspan=2)
tk.Button(frame, text="Sauvegarder", command=on_save).grid(row=9, columnspan=2)
tk.Button(frame, text="Exporter", command=on_export).grid(row=10, columnspan=2)
tk.Button(frame, text="Importer", command=on_import).grid(row=11, columnspan=2)
tk.Button(frame, text="Quitter", command=root.quit).grid(row=12, columnspan=2)

root.mainloop()
