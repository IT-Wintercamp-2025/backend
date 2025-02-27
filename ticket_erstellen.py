from flask import Flask, render_template, session, request, redirect, url_for, jsonify
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "0815"

def db_connection():
   
    connection = mysql.connector.connect(
        host="host.docker.internal",
        user="root",
        password="1234",
        database="backend"
    )
    return connection

@app.route("/ticket_hinzufuegen", methods=["GET", "POST"])
def ticket_hinzufuegen():
    if request.method == "POST":
        betreff = request.form["betreff"]
        beschreibung = request.form["Beschreibung"]
        team = request.form["Gruppe"]
        #benutzer_id = session['User']
        benutzer_id = 0
        erstellung = datetime.now().date()
        erstellung = erstellung.strftime("%d.%m.%Y")
        connection = db_connection()
        cursor = connection.cursor()
        sql2 = "SELECT Gruppen_id FROM gruppe WHERE Gruppenname = %s"
        cursor.execute(sql2, (team,))
        eintrag2 = cursor.fetchone()
        team_id = eintrag2[0]
        sql = "INSERT INTO ticket_data (Benutzer_id, Betreff, Beschreibung, Status, Team, Erstelldatum) VALUES (%s, %s,%s, %s, %s, %s)"
        val = (benutzer_id, betreff, beschreibung, 0, team_id, erstellung)
        cursor.execute(sql, val)
        connection.commit()
        return "Ticket erfolgreich erstellt"
    return render_template("Ticket_Formular.html")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)