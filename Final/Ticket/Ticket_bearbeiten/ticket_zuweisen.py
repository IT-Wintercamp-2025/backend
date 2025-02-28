from flask import Flask, render_template, session, request, redirect, url_for, jsonify
import mysql.connector
from datetime import datetime, timedelta
import pytz


def db_connection():
   
    connection = mysql.connector.connect(
        host="host.docker.internal",
        user="root",
        password="1234",
        database="backend"
    )
    return connection

@app.route("/ticket_zuweisen", methods=["GET", "POST"])
def ticket_zuweisen():
    if request.method == "POST":
        id1 = request.form=['ticket_id']
    #id1 = "1"
    try:
        connection = db_connection()
        cursor = connection.cursor()
        
        # Erster Query: Holen des Tickets
        sql = "SELECT * FROM ticket_data WHERE Ticket_id = %s"
        cursor.execute(sql, (id1,))
        eintrag = cursor.fetchone()

        # Holen des Enddatums aus der Sprint-Tabelle
        sql2 = "SELECT Datum_Ende FROM sprint WHERE Sprint_id = %s"
        cursor.execute(sql2, (eintrag[8],))
        eintrag2 = cursor.fetchone()
        datum = eintrag2[0]

        # Holen des Status-Namens
        sql3 = "SELECT anzeigename FROM status WHERE status_id = %s"
        cursor.execute(sql3, (eintrag[4],))
        eintrag3 = cursor.fetchone()
        status = eintrag3[0]

        # Holen der Priorität
        sql3 = "SELECT anzeigename FROM prio WHERE Prio_id = %s"
        cursor.execute(sql3, (eintrag[5],))
        eintrag3 = cursor.fetchone()
        prio = eintrag3[0]

        # Holen des Team-Namens
        sql3 = "SELECT gruppenname FROM gruppe WHERE Gruppen_id = %s"
        cursor.execute(sql3, (eintrag[6],))
        eintrag3 = cursor.fetchone()
        gruppe = eintrag3[0]

        # Holen der Kommentare zum Ticket
        sql3 = "SELECT * FROM kommentar WHERE Ticket_id = %s"
        cursor.execute(sql3, (id1,))
        eintrag4 = cursor.fetchall()

        # Liste für die modifizierten Kommentare
        neue_kommentare = []
        for kommentar in eintrag4:
            benutzer_id = kommentar[1]  # Benutzer-ID aus dem Kommentar
            
            # Benutzername aus der user_data-Tabelle holen
            sql4 = "SELECT Benutzername FROM user_data WHERE Benutzer_id = %s"
            cursor.execute(sql4, (benutzer_id,))
            eintrag5 = cursor.fetchone()

            if eintrag5:  # Falls ein Benutzer gefunden wurde
                name_kommentar = eintrag5[0]
            else:
                name_kommentar = "Unbekannt"

            # Neues Tupel mit ersetztem Namen erstellen
            neuer_kommentar = (kommentar[0], name_kommentar, kommentar[2], kommentar[3], kommentar[4])
            neue_kommentare.append(neuer_kommentar)
        return render_template("ticket_zuweisen.html", test=eintrag, test2=datum, test3=status, test4=prio, test5=gruppe, test6=neue_kommentare)

    except mysql.connector.Error as e:
        return "Fehler: " + str(e)


        
@app.route("/ticket_zuweisen_exe", methods=["GET", "POST"])
def ticket_zuweisen_exe():
    if request.method == "POST":
        benutzer_id = session['Benutzer_id']
        ticket_id = request.form["Ticket_id"]
        status = request.form["Status"]
        prio = request.form["Prio"]
        team = request.form["Team"]
        datum = request.form["Datum"]
        nachricht = request.form['Kommentar']
        # Berechnung des Sprints
        datum2 = datetime.strptime(datum, "%d.%m.%Y")
        tag = datum2.weekday()
        tag2 = 6 - tag
        enddatum = datum2 + timedelta(days=tag2)
        enddatum = enddatum.strftime("%d.%m.%Y")
        connection = db_connection()
        cursor = connection.cursor()

        timezone = pytz.timezone("Europe/Berlin")
        # Aktuelles Datum und Uhrzeit in der richtigen Zeitzone
        zeitstempel = datetime.now(timezone).strftime("%d.%m.%Y %H:%M:%S")

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

        if nachricht != "":
            sql = "INSERT INTO kommentar (user_id, Ticket_id, Nachricht, Zeitstempel) VALUES (%s, %s,%s, %s)"
            val = (benutzer_id, ticket_id, nachricht, zeitstempel)
            cursor.execute(sql, val)
            connection.commit()

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


    
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
