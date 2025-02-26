from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector
from datetime import datetime                                                 
import bcrypt 

def db_connection():                                                          
    try:
        connection = mysql.connector.connect(   
            host="mariadb",
            user="root",
            password="1234",
            database="IT_Camp"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Fehler: {err}")
        return None

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    
    if request.method == "POST":
        nutzer_name = request.form["nutzer_name"]
        passwort = request.form["passwort"]
        
        try:
            connection = db_connection()
            cursor = connection.cursor(buffered=True)
            cursor.execute("SELECT Passwort FROM Reg WHERE Benutzername = %s", (nutzer_name,))
            ergebniss = cursor.fetchone()

            if ergebniss:
                gesch_passwort = ergebniss[0]
                if bcrypt.checkpw(passwort.encode("utf-8"), gesch_passwort.encode("utf-8")):
                    session["nutzer_name"] = nutzer_name
                    return redirect(url_for("dashboard_show"))
                else:
                    message = "Falsches Passwort"
            else:
                message = "Benutzername nicht gefunden"
        except Exception as e:
            message = "Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut."
        finally:
            cursor.close()
            connection.close()
        
    return render_template("login.html", message=message)
