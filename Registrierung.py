import bcrypt
import json
import os
from datetime import datetime


def hash_passwort(passwort):
    return bcrypt.hashpw(passwort.encode("utf-8"), bcrypt.gensalt()).decode("utf-8") 

def set_role(user_id):
    if user_id == 0:
        return "admin"
    else:
        return "user"
    
def benutzername_eingabe():
    benutzername = str(input("Benutzername: "))
    benutzerdaten = benutzerdaten_laden()
     # Durchsuche die Benutzerdaten nach dem eingegebenen Benutzernamen
    benutzer_gefunden = False
    for benutzer in benutzerdaten:
        if benutzer["benutzername"] == benutzername:
            benutzer_gefunden = True
            print("Benutzername bereits vergeben.")
            return benutzername_eingabe()
        else:
            return benutzername

def passwort_eingabe():
    passwort = str(input("Passwort: "))
    passwort_bestätigung = str(input("Bitte Passwort bestätigen:"))
    try:
        if passwort_bestätigung == passwort:
            return hash_passwort(passwort)
        else:
            print("Passwörter stimmen nicht überein")
            return None
    except:
        raise NameError("Es sollte nicht möglich sein diesen Fehler zu bekommen :)")
    
def benutzerdaten_laden():
    try:
        with open("benutzerdaten.json", "r") as datei:
            benutzerdaten = json.load(datei)
        return benutzerdaten
    except FileNotFoundError:
        print("Die Datei 'benutzerdaten.json' wurde nicht gefunden.")
        return None
    except json.JSONDecodeError:
        print("Die Datei 'benutzerdaten.json' enthält ungültigen JSON.")
        return None

def benutzerdaten_speichern(benutzername, hashed_passwort):
    # Überprüfen, ob die Datei existiert und nicht leer ist
    if os.path.exists("benutzerdaten.json") and os.path.getsize("benutzerdaten.json") > 0:
        with open("benutzerdaten.json", "r") as datei:
            try:
                benutzerdaten = json.load(datei)
            except json.JSONDecodeError:
                # Falls die Datei ungültigen JSON enthält, initialisiere eine leere Liste
                benutzerdaten = []
    else:
        # Wenn die Datei nicht existiert oder leer ist, initialisiere eine leere Liste
        benutzerdaten = []
    
    # Neuen Benutzer hinzufügen
    neuer_benutzer = {
        "benutzername": benutzername,
        "hashed_passwort": hashed_passwort,
        "Registriert am": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    benutzerdaten.append(neuer_benutzer)
    
    # Alle Benutzerdaten speichern
    with open("benutzerdaten.json", "w") as datei:
        json.dump(benutzerdaten, datei, indent=4)


benutzername = benutzername_eingabe()
hashed_passwort = passwort_eingabe()

if hashed_passwort:
    benutzerdaten_speichern(benutzername, hashed_passwort)
    print("")
    print("Benutzerdaten wurden gespeichert.")
    print("Benutzername:", benutzername)
    print("Passwort:", hashed_passwort)
