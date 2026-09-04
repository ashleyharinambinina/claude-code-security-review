"""
FICHIER DE TEST -- contient des vulnérabilités INTENTIONNELLES
Objectif : valider que le scanner de sécurité (Claude Code Security Review)
détecte bien ces failles classiques. Ne jamais utiliser ce code en production.
"""

import os
import sqlite3
import subprocess
import pickle
import hashlib

# --- 1. Secret codé en dur ---
API_KEY = "sk-live-51Hxa8kFj29dKq7z8pQwErTyUiOpAsDfGhJk"
DB_PASSWORD = "SuperSecret123!"


# --- 2. Injection SQL ---
def get_user(username):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()


# --- 3. Injection de commande OS ---
def ping_host(host):
    command = f"ping -c 1 {host}"
    result = subprocess.run(command, shell=True, capture_output=True)
    return result.stdout


# --- 4. Désérialisation non sécurisée (RCE potentiel) ---
def load_user_session(session_data):
    return pickle.loads(session_data)


# --- 5. eval() sur une entrée utilisateur ---
def calculate(expression):
    return eval(expression)


# --- 6. Hachage de mot de passe faible ---
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


# --- 7. Path traversal ---
def read_user_file(filename):
    path = os.path.join("/var/app/uploads/", filename)
    with open(path, "r") as f:
        return f.read()


# --- 8. XXE potentiel (parsing XML non sécurisé) ---
def parse_xml(xml_string):
    import xml.etree.ElementTree as ET
    tree = ET.fromstring(xml_string)
    return tree


if __name__ == "__main__":
    print(get_user(input("Username: ")))