import json
import bcrypt
from flask import Flask, request, session

app = Flask(__name__)
app.secret_key = "0815"

def check_passwort():
    # Lade die Benutzerdaten aus der JSON-Datei
    benutzerdaten = benutzerdaten_laden()
    
    if not benutzerdaten:
        print("Keine Benutzerdaten gefunden.")
        return
    
    # Benutzereingabe
    check_benutzername = input("Benutzername: ")
    check_passwort = input("Passwort: ")
    
    # Durchsuche die Benutzerdaten nach dem eingegebenen Benutzernamen
    benutzer_gefunden = False
    for benutzer in benutzerdaten:
        if benutzer["benutzername"] == check_benutzername:
            benutzer_gefunden = True
            # Überprüfe das Passwort
            if bcrypt.checkpw(check_passwort.encode("utf-8"), benutzer["hashed_passwort"].encode("utf-8")):
                print("Anmeldung erfolgreich!")
            else:
                print("Falsches Passwort.")
            break
    
    if not benutzer_gefunden:
        print("Benutzername nicht gefunden.")

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

# Starte die Passwortüberprüfung
check_passwort()
