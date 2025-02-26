import json
import bcrypt
import mysql.connector
from flask import Flask, request, session

app = Flask(__name__)
app.secret_key = "0815"

def db_connection():
    connection = mysql.connector.connect(
        host="host.docker.internal",
        user="root",
        password="1234",
        database="testDB"
    )
    return connection

@app.route('/auth/login', methods=['POST'])
def login():
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM benutzer WHERE benutzername = %s", (request.form["benutzername"],))
    # Starte die Passwortüberprüfung
    check_passwort(cursor,request)

def check_passwort(cursor,request):
    user = get_user(cursor,request)
    if user is not None and len(user) > 0:
        # Überprüfe das Passwort
        if bcrypt.checkpw(request.form["passwort"].encode("utf-8"), user[0][2].encode("utf-8")):
            return "Anmeldung erfolgreich", 200
        else:
            # Passwort falsch
            return "Anmeldung fehlgeschlagen", 401
    else:
        # Benutzer nicht gefunden
        return "Anmeldung fehlgeschlagen", 401

def get_user(cursor,request):
    try:
        cursor.execute("SELECT * FROM benutzer WHERE benutzername = %s", (request.form["benutzername"],))
        benutzer = cursor.fetchall()
        return benutzer
    except Exception as e:
        return None

