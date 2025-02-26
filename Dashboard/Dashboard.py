from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def db_connection():
    try:
        connection = mysql.connector.connect(
            host="host.docker.internal",
            user="root",
            password="1234",
            database="Backend"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Fehler: {err}")
        return None

@app.route("/Ticket_Uebersicht", methods = ["GET", "POST"])
def dashboard():
    ticket = []
    try:
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT Ticket_id, Betreff, Benutzername, Beschreibung, Status, Prio, Team, Erstelldatum, Sprint \
                       FROM ticket_data\
                       INNER JOIN user_data \
                       ON ticket_data.Benutzer_id = user_data.Benutzer_id")
        ticket = cursor.fetchall()
        return render_template("Ticket_Uebersicht.html", ticket=ticket)
    except Exception as e:
        return f"Fehler: {e}"
    finally: 
        cursor.close()
        connection.close()
    
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
