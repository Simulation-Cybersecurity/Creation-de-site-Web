from flask import Flask, request, render_template_string, send_file
import sqlite3
import os
import pickle
import base64
import random

# Initialisation de l'application Flask
# Note : Flask 0.10.1 est vulnérable à plusieurs failles de session
app = Flask(__name__)

# --- 1. SQL INJECTION (Ton code original) ---
def login_user(username, password):
    # CWE-89 : Concaténation directe d'entrées utilisateur dans une requête SQL
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    cursor.execute(query)
    return cursor.fetchone()

# --- 2. COMMAND INJECTION (Ton code original) ---
def backup_logs(filename):
    # CWE-78 : Utilisation de os.system avec une entrée non filtrée
    # Un attaquant pourrait envoyer "file.txt ; rm -rf /"
    print("Sauvegarde des logs...")
    os.system("cp logs.txt " + filename)

# --- 3. CROSS-SITE SCRIPTING (XSS) ---
@app.route('/profile')
def profile():
    # CWE-79 : Injection de données utilisateur dans un template sans échappement
    # Test : /profile?name=<script>alert('Hacked')</script>
    name = request.args.get('name', 'Guest')
    return render_template_string(f"<h1>Profil de {name}</h1>")

# --- 4. INSECURE DESERIALIZATION (RCE) ---
@app.route('/load-settings')
def load_settings():
    # CWE-502 : Utilisation de pickle sur des données externes
    # Cela permet d'exécuter n'importe quel code sur le serveur
    data = request.args.get('data')
    if data:
        decoded_data = base64.b64decode(data)
        settings = pickle.loads(decoded_data)
        return "Configuration chargée !"
    return "En attente de données..."

# --- 5. PATH TRAVERSAL (Lecture de fichiers arbitraires) ---
@app.route('/view-file')
def view_file():
    # CWE-22 : L'utilisateur peut remonter dans l'arborescence
    # Test : /view-file?path=../../../../etc/passwd
    file_path = request.args.get('path')
    return send_file(file_path)

# --- 6. INSUFFICIENTLY RANDOM VALUES ---
@app.route('/reset-password')
def reset_password():
    # CWE-330 : Utilisation de random.random() pour de la cryptographie
    # Les tokens générés ainsi sont prévisibles
    token = str(random.random())
    return f"Votre token de réinitialisation : {token}"

# --- 7. HARDCODED CREDENTIALS ---
@app.route('/admin-check')
def admin_check():
    # CWE-798 : Mot de passe écrit en dur dans le code
    SECRET_ADMIN_KEY = "SECRET_12345_ABCDE"
    user_key = request.args.get('key')
    if user_key == SECRET_ADMIN_KEY:
        return "Accès admin autorisé."
    return "Accès refusé."

if __name__ == "__main__":
    # CWE-489 : Le mode Debug permet l'exécution de code à distance via la console interactive
    app.run(debug=True, port=5000)
