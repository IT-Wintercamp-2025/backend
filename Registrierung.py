import bcrypt
import json
from datetime import datetime
from flask import Flask, request, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "0815"

def db_connection():
    connection = mysql.connector.connect(
        host="host.docker.internal",
        user="root",
        password="1234",
        database="Backend"
    )
    return connection

@app.route('/auth/register', methods=['POST'])
def register():
    connection = None
    cursor = None
    try:
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data WHERE Benutzername = %s", (request.form["Benutzername"],))
        # Starte die Passwortüberprüfung
        benutzername = benutzername_eingabe(cursor,request)
        hashed_passwort = passwort_eingabe(cursor,request)

        if hashed_passwort:
            benutzerdaten_speichern(benutzername, hashed_passwort,cursor,connection)
            print("")
            print("Benutzerdaten wurden gespeichert.")
            print("Benutzername:", benutzername)
            print("Passwort:", hashed_passwort)
    except Exception as e:
        return "Verbindung fehlgeschlagen", 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def hash_passwort(passwort):
    return bcrypt.hashpw(passwort.encode("utf-8"), bcrypt.gensalt()).decode("utf-8") 

def set_role(user_id):
    if user_id == 0:
        session["rolle"] = 2
        return 2 # Admin
    else:
        session["rolle"] = 0
        return 0 # Guest
    
def validate_username(benutzername):
    if len(benutzername) < 3: # Der Benutzername muss mindestens 3 Zeichen lang sein
        return False, "Der Benutzername muss mindestens 3 Zeichen lang sein."
    elif len(benutzername) > 20: # Der Benutzername darf maximal 20 Zeichen lang sein
        return False, "Der Benutzername darf maximal 20 Zeichen lang sein."
    elif not benutzername.isalnum(): # Der Benutzername darf nur Buchstaben und Zahlen enthalten
        return False, "Der Benutzername darf nur Buchstaben und Zahlen enthalten."
    elif not benutzername[0].isalpha(): # Der Benutzername muss mit einem Buchstaben beginnen
        return False, "Der Benutzername muss mit einem Buchstaben beginnen."
    else:
        return True,None
    
    
def benutzername_eingabe(cursor,request):
    #benutzername = request.form["Benutzername"]
    benutzername = input("Bitte Benutzername eingeben:")
    is_name_valid, errormessage = validate_username(benutzername)
    while not is_name_valid:
        print(errormessage)
        #benutzername = request.form["Benutzername"]
        benutzername = input("Bitte Benutzername eingeben:")
        is_name_valid, errormessage = validate_username(benutzername)
    benutzerdaten = benutzerdaten_laden(cursor,request)
    # Durchsuche die Benutzerdaten nach dem eingegebenen Benutzernamen
    for benutzer in benutzerdaten:
        if benutzer["Benutzername"] == benutzername:
            print("Benutzername bereits vergeben.")
            return benutzername_eingabe(cursor,request)
    return benutzername
        
def check_passwort_streanght(passwort):
    if len(passwort) < 4:
        print("Passwort muss mindestens 4 Zeichen lang sein.")
        return False
    else:
        return True        

def passwort_eingabe(cursor,request):
    #passwort = request.form["Passwort"]
    passwort = input("Bitte Passwort eingeben:")
    while not check_passwort_streanght(passwort):
        #passwort = request.form["Passwort"]
        passwort = input("Bitte Passwort eingeben:")
    #passwort_bestätigung = request.form["passwort_bestätigung"]
    passwort_bestätigung = input("Bitte Passwort bestätigen:")
    try:
        if passwort_bestätigung == passwort:
            return hash_passwort(passwort)
        else:
            print("Passwörter stimmen nicht überein")
            return None
    except:
        raise NameError("Es sollte nicht möglich sein diesen Fehler zu bekommen :)")
    
def benutzerdaten_laden(cursor,request):
    cursor.execute("SELECT * FROM benutzer")
    benutzerdaten = []
    for benutzer in cursor.fetchall():
        benutzerdaten.append({
            "id": benutzer[0],
            "benutzername": benutzer[1],
            "passwort": benutzer[2]
        })
    return benutzerdaten
   

def benutzerdaten_speichern(benutzername, hashed_passwort,cursor,connection):
    cursor.execute("INSERT INTO user_data (Benutzername, Passwort) VALUES (%s, %s)", (benutzername, hashed_passwort))
    connection.commit()
    

register()

    
