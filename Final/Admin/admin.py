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


#@app.route("/benutzer_verwaltung")
#def benutzer_verwaltung():
#    connection = db_connection()
#    cursor = connection.cursor()
#    cursor.execute("SELECT * FROM user_data")
#    myresult = cursor.fetchall()  # Gibt eine Liste von Tupeln zurück
#
#    updated_result = []
#    for row in myresult:
#        user_list = list(row)  # Konvertiere das Tupel in eine Liste, damit es veränderbar ist
#        sql2 = "SELECT Gruppenname FROM gruppe WHERE Gruppen_id = %s"
#        cursor.execute(sql2, (row[4],)) 
#        eintrag2 = cursor.fetchone()
#        if eintrag2:
#            user_list[4] = eintrag2[0]
#        updated_result.append(user_list)
#
#    return render_template("benutzer_verwaltung.html", myresult=updated_result)

@app.route("/benutzer_verwaltung", methods=["GET", "POST"])
def benutzer_verwaltung():
    search_query = request.args.get('search_query', '')  # Hole die Suchanfrage
    search_column = request.args.get('search_column', 'name')  # Hole die Spalte, nach der gesucht werden soll
    connection = db_connection()
    cursor = connection.cursor()

    # Definiere, nach welcher Spalte gesucht wird
    if search_column == 'id':
        search_field = 'Benutzer_id'
    elif search_column == 'name':
        search_field = 'Benutzername'
    elif search_column == 'zugeteiltes_team':
        search_field = 'Gruppe'
    elif search_column == 'rolle':
        search_field = 'Rolle'
    elif search_column == 'gesperrt':
        search_field = 'Sperren'
    else:
        search_field = 'Benutzername'  # Default-Fall

    # Hole alle Benutzerdaten
    cursor.execute(f"SELECT * FROM user_data WHERE {search_field} LIKE %s", ('%' + search_query + '%',))
    myresult = cursor.fetchall()

    # Aktualisiere die Benutzerdaten mit Gruppenname
    updated_result = []
    for row in myresult:
        user_list = list(row)  # Konvertiere das Tupel in eine Liste
        sql2 = "SELECT Gruppenname FROM gruppe WHERE Gruppen_id = %s"
        cursor.execute(sql2, (row[4],))
        eintrag2 = cursor.fetchone()
        if eintrag2:
            user_list[4] = eintrag2[0]
        updated_result.append(user_list)

    return render_template("benutzer_verwaltung.html", myresult=updated_result)

@app.route("/benutzer_sperren", methods=["GET", "POST"])
def benutzer_sperren():
    if request.method == "POST":
        user_id = request.form["user_id"]
    connection = db_connection()
    cursor = connection.cursor()
    sql = "UPDATE user_data SET Sperren = 1 WHERE Benutzer_id = %s"
    val = ((user_id),)
    cursor.execute(sql, val)
    connection.commit()
    return benutzer_verwaltung()


@app.route("/benutzer_entsperren", methods=["GET", "POST"])
def benutzer_entsperren():
    if request.method == "POST":
        user_id = request.form["user_id"]
    connection = db_connection()
    cursor = connection.cursor()
    sql = "UPDATE user_data SET Sperren = 0 WHERE Benutzer_id = %s"
    val = ((user_id),)
    cursor.execute(sql, val)
    connection.commit()
    return benutzer_verwaltung()

@app.route("/benutzer_loeschen", methods=['GET', "POST"])
def benutzer_loeschen():
    if request.method == "POST":
        user_id = request.form['user_id']
    connection = db_connection()
    cursor = connection.cursor()
    sql = "DELETE FROM user_data WHERE Benutzer_id = %s"
    cursor.execute(sql, (user_id,))
    connection.commit()
    return benutzer_verwaltung()

@app.route("/benutzer_bearbeiten", methods=["GET", "POST"])
def benutzer_bearbeiten():
    if request.method == "POST":
        user_id = request.form['user_id']
    connection = db_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM user_data WHERE Benutzer_id = %s"
    val = ((user_id),)
    cursor.execute(sql, val)
    test2 = cursor.fetchone()

    sql = "SELECT Gruppenname FROM gruppe WHERE Gruppen_id = %s"
    val = ((test2[4]),)
    cursor.execute(sql, val)
    test3 = cursor.fetchone()
    test3 = test3[0]

    return render_template("benutzer_verwaltung_bearbeiten.html", test = test2, test2=test3)

@app.route("/benutzer_bearbeiten_exe", methods=["GET", "POST"])
def benutzer_bearbeiten_exe():
    if request.method == "POST":
        user_id = request.form["user_id"]
        name = request.form["Name"]
        gruppe = request.form["Gruppe"]
        rolle = request.form["Rolle"]

        connection = db_connection()
        cursor = connection.cursor()
        sql2 = "SELECT Gruppen_id FROM gruppe WHERE Gruppenname = %s"
        cursor.execute(sql2, (gruppe,))
        eintrag2 = cursor.fetchone()
        gruppen_id = eintrag2[0]
        email = ""

        connection = db_connection()
        cursor = connection.cursor()
        sql = "UPDATE user_data SET Benutzername = %s, EMail = %s, Gruppe = %s, Rolle = %s WHERE Benutzer_id = %s"

        val = (name, email, gruppen_id, rolle, user_id)

        try:
            cursor.execute(sql, val)
            connection.commit()
            return benutzer_verwaltung()
        except Exception as e:
            connection.rollback()
            return f"Fehler: {str(e)}"
    return render_template("ticket_zuweisen.html")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
