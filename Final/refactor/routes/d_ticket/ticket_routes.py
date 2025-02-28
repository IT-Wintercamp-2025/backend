from flask import render_template, Blueprint, request
import mysql.connector

tickets_blueprint = Blueprint("tickets", __name__, template_folder="templates")

def db_connection():
    try:
        connection = mysql.connector.connect(
            host="ticketsystem-database-1", # vor Ende zur Finalen Datenbank ändern
            user="root",                    # vor Ende ändern
            password="1234",                # vor Ende ändern
            database="backend"              # vor Ende zur Finalen Datenbank ändern
        )
        return connection
    except mysql.connector.Error as error:
        print("Fehler bei der Datenbankverbindung:", error)
        return None

@tickets_blueprint.route("/ticket/ticket_ausgabe")
def ticket_ausgabe():
    ticket_id = 3 # frontend muss das abgreifen
    try:
        connection = db_connection()
        cursor = connection.cursor()

        ##Daten von DB ziehen
        # fertige Daten (Ticket ID	Betreff 	Beschreibung und Erstellungsdatum) aus DB ziehen
        cursor.execute("SELECT Ticket_id, Betreff, Beschreibung, Erstelldatum FROM ticket_data WHERE Ticket_id = %s", (ticket_id,))
        test = cursor.fetchall()

        # ID-Daten (Status 	Priorität 	Fachabteilung (Team) aus DB ziehen und umwandeln.
        cursor.execute("SELECT status.anzeigename FROM ticket_data JOIN status ON ticket_data.Status = status.status_id WHERE ticket_data.Ticket_id = %s", (ticket_id,))
        test2 = cursor.fetchall()
        transfer1 = test2[0][0] if test2 else ("Keinen") #test 2 aus tulpe in normal umwandeln

        cursor.execute("SELECT prio.anzeigename FROM ticket_data JOIN prio ON ticket_data.Prio = prio.prio_id WHERE ticket_data.Ticket_id = %s", (ticket_id,))
        test3 = cursor.fetchall()
        transfer2 = test3[0][0] if test3 else ("Keine")

        cursor.execute("SELECT gruppe.Gruppenname FROM ticket_data JOIN gruppe ON ticket_data.Team = gruppe.Gruppen_id WHERE ticket_data.Ticket_id = %s", (ticket_id,))
        test4 = cursor.fetchall()
        transfer3 = test4[0][0] if test4 else ("Keine")

        cursor.execute("SELECT Betreff FROM ticket_data WHERE Ticket_id = %s", (ticket_id,))
        betreff = cursor.fetchall()
        neu = betreff[0][0] if betreff else ("Keinen")

        cursor.execute("SELECT Beschreibung FROM ticket_data WHERE Ticket_id = %s", (ticket_id,))
        beschreibung = cursor.fetchall()
        neu2 = beschreibung[0][0] if beschreibung else ("Keine")

        return render_template('ticket_einsicht.html', ticket_data=test, transfer1=transfer1, transfer2=transfer2, transfer3=transfer3, neu=neu, neu2=neu2)
    except Exception as e:
        return f"Fehler: {e}"


@tickets_blueprint.route('/tickets')
def ticket_bearbeiten():
    ticket_id = 3 # frontend muss das abgreifen

    try:
        connection = db_connection()
        cursor = connection.cursor()

        # Daten aus dem Formular in die DB
        Betreff = request.form["betreff_e"]
        Beschreibung = request.form["beschreibung_e"]
        sql1 = "UPDATE ticket_data SET Betreff = %s WHERE Ticket_id = %s"
        sql2 = "UPDATE ticket_data SET Beschreibung = %s WHERE Ticket_id = %s"
        cursor.execute(sql1, (Betreff, ticket_id))
        cursor.execute(sql2, (Beschreibung, ticket_id))
        connection.commit()

        cursor.execute("SELECT Ticket_id, Betreff, Beschreibung, Erstelldatum FROM ticket_data WHERE Ticket_id = %s", (ticket_id,))
        test = cursor.fetchall()

        # Ticket geupdatet zeigen
        # ID-Daten (Status 	Priorität 	Fachabteilung (Team) aus DB ziehen und umwandeln.
        cursor.execute("SELECT status.anzeigename FROM ticket_data JOIN status ON ticket_data.Status = status.status_id WHERE ticket_data.Ticket_id = %s", (ticket_id,))
        test2 = cursor.fetchall()
        transfer1 = test2[0][0] if test2 else ("Keinen") #test 2 aus tulpe in normal umwandeln

        cursor.execute("SELECT prio.anzeigename FROM ticket_data JOIN prio ON ticket_data.Prio = prio.prio_id WHERE ticket_data.Ticket_id = %s", (ticket_id,))
        test3 = cursor.fetchall()
        transfer2 = test3[0][0] if test3 else ("Keine")

        cursor.execute("SELECT gruppe.Gruppenname FROM ticket_data JOIN gruppe ON ticket_data.Team = gruppe.Gruppen_id WHERE ticket_data.Ticket_id = %s", (ticket_id,))
        test4 = cursor.fetchall()
        transfer3 = test4[0][0] if test4 else ("Keine")

        cursor.execute("SELECT Betreff FROM ticket_data WHERE Ticket_id = %s", (ticket_id,))
        betreff = cursor.fetchall()
        neu = betreff[0][0] if betreff else ("Keinen")

        cursor.execute("SELECT Beschreibung FROM ticket_data WHERE Ticket_id = %s", (ticket_id,))
        beschreibung = cursor.fetchall()
        neu2 = beschreibung[0][0] if beschreibung else ("Keine")

        return render_template('ticket_einsicht.html', ticket_data=test, transfer1=transfer1, transfer2=transfer2, transfer3=transfer3, neu=neu, neu2=neu2)

    except Exception as e:
        return f"Fehler: {e}"
    finally:
        if connection:
            connection.close()


def register_routes(app):
    app.register_blueprint(tickets_blueprint)
