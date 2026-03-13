import sqlite3
import os

def login_user(username, password):
    # DANGER : Concaténation de chaîne pour une requête SQL
    # Snyk va détecter une "SQL Injection"
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    cursor.execute(query)
    return cursor.fetchone()

def backup_logs(filename):
    # DANGER : Utilisation de os.system avec une entrée utilisateur
    # Snyk va détecter une "Command Injection"
    print("Sauvegarde des logs...")
    os.system("cp logs.txt " + filename)

# Simulation d'utilisation
user_input = "admin' OR '1'='1" # Exemple d'attaque SQL
login_user(user_input, "password123")
