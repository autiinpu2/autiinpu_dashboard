import hashlib
import json
import os

users = {}
def hash_sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

def add_user_to_json(username, password, filename="users.json"):
    """Ajoute un utilisateur haché à users.json."""
    hashed_username = hash_sha256(username)
    hashed_password = hash_sha256(password)

    # Vérifier si le fichier existe et s'il est vide
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        users = {}  # Initialiser un dictionnaire vide
    else:
        try:
            with open(filename, 'r') as file:
                users = json.load(file)
        except json.JSONDecodeError:
            print("Erreur : Le fichier JSON est corrompu. Réinitialisation...")
            users = {}  # Réinitialiser le dictionnaire

    # Ajouter l'utilisateur haché
    users[hashed_username] = hashed_password

    # Sauvegarder le fichier mis à jour
    with open(filename, 'w') as file:
        json.dump(users, file, indent=4)

    print(f"Utilisateur {username} ajouté avec succès.")

def load_users_from_json(filename="users.json"):
    """Charge les utilisateurs depuis users.json et retourne un dictionnaire."""
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return {}  # Retourne un dictionnaire vide si le fichier n'existe pas ou est vide

    try:
        with open(filename, 'r') as file:
            users = json.load(file)
        return users
    except json.JSONDecodeError:
        print("Erreur : Le fichier JSON est corrompu. Réinitialisation...")
        return {}  # Réinitialiser un dictionnaire vide en cas d'erreur

users = load_users_from_json()

def check_if_user_in_ddb(username, password):
    
    hash_username = hash_sha256(username)
    hash_password = hash_sha256(password)

    if hash_username in users:
        if users[hash_username] == hash_password:
            return True
        else:
            return False, "Password incorrect"
    else:
        return False, "user not found"

