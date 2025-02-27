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

@app.route('/rechte')
def hello():
    try:
        rolle = session['rolle']
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")
        test = cursor.fetchall()
        #return test
        if rolle >= 0:
            test4 = "Du hast folgende Rechte: Ticket erstellen, eigene Tickets einsehen, eigene Tickets bearbieten"
        if rolle >= 1:
            test4 += " Du hast folgende Rechte: Tickets zuweisen, Prio, Status und Sprint Bearbeitung"
        if rolle >= 2:
             test4 += " Du hast folgende Rechte: Benutzer verwalten, Sperren, PW zurücksetzten, Gruppen zuweisen"
        return test4
    
    except Exception as e:
        return f"Fehler: {e}"
@app.route('/2')
def hello2():
    session['rolle'] = 1
    return "1"
@app.route('/3')
def abbruch():
    session.pop("rolle", None)
    return "1"


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

@app.route("/sprint_hinzufuegen")
def sprint_hinzufuegen():
    jahr = datetime.now().year
    start_daten = []
    end_daten = []
    connection = db_connection()
    cursor = connection.cursor()
    sql = "DELETE FROM sprint"
    cursor.execute(sql)
    connection.commit()
    for woche in range(1, 54):
        try:
            erster_tag = datetime.strptime(f"{jahr}-W{woche}-1", "%Y-W%W-%w")
            letzter_tag = erster_tag + timedelta(days=6)
            if letzter_tag.year != jahr and woche > 50:
                break
            erster_tag = erster_tag.strftime("%d.%m.%Y")
            letzter_tag = letzter_tag.strftime("%d.%m.%Y")
            sql = "INSERT INTO sprint (Datum_Beginn, Datum_Ende) VALUES (%s, %s)"
            val = (erster_tag, letzter_tag)
            cursor.execute(sql, val)
            connection.commit()

        except ValueError:
            break 
    return "Sprints für das Jahr erfolgrecih hinzugefügt"

@app.route("/ticket_zuweisen")
def ticket_zuweisen():
    id1 = "1"
    try:
        connection = db_connection()
        cursor = connection.cursor()
        
        # Erster Query: Holen des Tickets
        sql = "SELECT * FROM ticket_data WHERE Ticket_id = %s"
        cursor.execute(sql, (id1,))
        eintrag = cursor.fetchone()

        # Zweiter Query: Holen des Enddatums aus der Sprint-Tabelle
        sql2 = "SELECT Datum_Ende FROM sprint WHERE Sprint_id = %s"
        cursor.execute(sql2, (eintrag[8],))  # Beachte hier die Übergabe des richtigen Parameters
        eintrag2 = cursor.fetchone()
        datum = eintrag2[0]

        # Zweiter Query: Holen des Enddatums aus der Sprint-Tabelle
        sql3 = "SELECT anzeigename FROM status WHERE status_id = %s"
        cursor.execute(sql3, (eintrag[4],))  # Beachte hier die Übergabe des richtigen Parameters
        eintrag3 = cursor.fetchone()
        status = eintrag3[0]

        # Zweiter Query: Holen des Enddatums aus der Sprint-Tabelle
        sql3 = "SELECT anzeigename FROM prio WHERE Prio_id = %s"
        cursor.execute(sql3, (eintrag[5],))  # Beachte hier die Übergabe des richtigen Parameters
        eintrag3 = cursor.fetchone()
        prio = eintrag3[0]

        
        # Zweiter Query: Holen des Enddatums aus der Sprint-Tabelle
        sql3 = "SELECT gruppenname FROM gruppe WHERE Gruppen_id = %s"
        cursor.execute(sql3, (eintrag[6],))  # Beachte hier die Übergabe des richtigen Parameters
        eintrag3 = cursor.fetchone()
        gruppe = eintrag3[0]
        
        return render_template("ticket_zuweisen.html", test=eintrag, test2=datum, test3=status, test4=prio, test5=gruppe)

    except mysql.connector.Error as e:
        return "Fehler: " + str(e)

@app.route("/ticket_zuweisen_exe", methods=["GET", "POST"])
def ticket_zuweisen_exe():
    if request.method == "POST":
        ticket_id = request.form["Ticket_id"]
        status = request.form["Status"]
        prio = request.form["Prio"]
        team = request.form["Team"]
        datum = request.form["Datum"]
        # Berechnung des Sprints
        datum2 = datetime.strptime(datum, "%d.%m.%Y")
        tag = datum2.weekday()
        tag2 = 6 - tag
        enddatum = datum2 + timedelta(days=tag2)
        enddatum = enddatum.strftime("%d.%m.%Y")
        connection = db_connection()
        cursor = connection.cursor()

        sql2 = "SELECT Sprint_id FROM sprint WHERE Datum_Ende = %s"
        cursor.execute(sql2, (enddatum,))
        eintrag2 = cursor.fetchone()
        sprint_id = eintrag2[0]

        sql2 = "SELECT status_id FROM status WHERE anzeigename = %s"
        cursor.execute(sql2, (status,))
        eintrag2 = cursor.fetchone()
        status_id = eintrag2[0]

        sql2 = "SELECT Prio_id FROM prio WHERE anzeigename = %s"
        cursor.execute(sql2, (prio,))
        eintrag2 = cursor.fetchone()
        prio_id = eintrag2[0]

        sql2 = "SELECT Gruppen_id FROM gruppe WHERE Gruppenname = %s"
        cursor.execute(sql2, (team,))
        eintrag2 = cursor.fetchone()
        gruppen_id = eintrag2[0]

        connection = db_connection()
        cursor = connection.cursor()
        sql = "UPDATE ticket_data SET Status = %s, Prio = %s, Team = %s, Sprint = %s WHERE Ticket_id = %s"

        val = (status_id, prio_id, gruppen_id, sprint_id, ticket_id)

        try:
            cursor.execute(sql, val)
            connection.commit()
            return ticket_zuweisen()
        except Exception as e:
            connection.rollback()
            return f"Fehler: {str(e)}"
    return render_template("ticket_zuweisen.html")
    
@app.route("/benutzer_verwaltung")
def benutzer_verwaltung():
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")
    myresult = cursor.fetchall()
    #return myresult

    sql2 = "SELECT Gruppenname FROM gruppe WHERE Gruppen_id = %s"
    cursor.execute(sql2, (1,))
    eintrag2 = cursor.fetchone()
    #myresult[4] = eintrag2[0]

    return render_template("benutzer_verwaltung.html", myresult = myresult)

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
    return render_template("benutzer_verwaltung_bearbeiten.html", test = test2)

@app.route("/benutzer_bearbeiten_exe", methods=["GET", "POST"])
def benutzer_bearbeiten_exe():
    return "1"

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)