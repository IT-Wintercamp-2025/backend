from flask import Flask, session, render_template, redirect, request, url_for
import mysql.connector
import bcrypt
import re

app = Flask(__name__)
app.secret_key = '0815'

def db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="Backend3"
        )
        return connection
    except mysql.connector.Error as e:
        print("Fehler bei der Datenbankverbindung:", e)
        return None

@app.route('/SignUp', methods=['GET', 'POST'])
def register():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        passwort = request.form["password"]
        passwort_bestaetigen = request.form["password_be"]

        if len(passwort) < 4:
            message = "Das Passwort muss mindestens 4 Zeichen lang sein!"
            return render_template('SignUp.html', message=message)

        if len(username) < 3:
            message = "Der Benutzername muss mindestens 3 Zeichen lang sein!"
            return render_template('SignUp.html', message=message)
        
        if len(username) > 20:
            message = "Der Benutzername darf maximal 20 Zeichen lang sein!"
            return render_template('SignUp.html', message=message)

        if not re.match("^[A-Za-z0-9]+$", username):
            message = "Der Benutzername darf nur Buchstaben und Zahlen enthalten!"
            return render_template('SignUp.html', message=message)

        if passwort != passwort_bestaetigen:
            message = "Die Passwörter stimmen nicht überein!"
            return render_template('SignUp.html', message=message)

        try:
            connection = db_connection()
            if connection is None:
                message = "Datenbankverbindung fehlgeschlagen!"
                return render_template('SignUp.html', message=message)

            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM user_data WHERE Benutzername = %s", (username,))
            count = cursor.fetchone()[0]
            if count > 0:
                message = "Der Benutzername ist bereits vergeben!"
                return render_template('SignUp.html', message=message)

            cursor.execute("SELECT COUNT(*) FROM user_data")
            user_count = cursor.fetchone()[0]

            rolle = 2 if user_count == 0 else 0
            gruppe = 4

            hashed_passwort = bcrypt.hashpw(passwort.encode("utf-8"), bcrypt.gensalt())

            cursor.execute(
                "INSERT INTO user_data (Benutzername, Passwort, Email, Gruppe, Rolle) VALUES (%s, %s, %s, %s, %s)",
                (username, hashed_passwort, username+"@email.com", gruppe, rolle)
            )
            connection.commit()
            cursor.execute("SELECT Benutzer_id FROM user_data WHERE Benutzername = %s", (username,))
            user_id = cursor.fetchone()[0]
            session['Benutzer_id'] = user_id
            message = "Registrierung erfolgreich!"
            return render_template('SignUp.html', message=message)
        except Exception as e:
            message = f"Fehler: {e}"
            print(e)
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    return render_template('SignUp.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        connection = db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            
            # Fetch the user data first
            cursor.execute('SELECT * FROM user_data WHERE Benutzername = %s', (username,))
            user = cursor.fetchone()

            if user:
                # Check if the user is locked
                if user['Sperren'] == 1:
                    if user['Rolle'] != 2:
                        message = 'Dieser Nutzer wurde gesperrt!'
                        cursor.close()
                        connection.close()
                        return render_template('Login.html', message=message)
                    else:
                        # Admin is locked, but still allowed to proceed
                        session['locked_message'] = 'Du wurdest als Admin gesperrt, womöglich wurde das System gehackt!'

                # Check the password
                if bcrypt.checkpw(password.encode('utf-8'), user['Passwort'].encode('utf-8')):
                    session['loggedin'] = True
                    session['Benutzer_id'] = user['Benutzer_id']
                    if user['Rolle'] == 2:
                        return redirect(url_for('admin_dashboard'))  # Hier das HTML vom Admin Dashboard
                    elif user['Rolle'] == 1:
                        return render_template('employee_dashboard.html')   # Hier das HTML vom Mitarbeiter Dashboard
                    else:
                        return render_template('guest_dashboard.html')   # Hier das HTML vom Gast Dashboard
                else:
                    message = 'Falsches Passwort!'
            else:
                message = 'Benutzer existiert nicht!'
            cursor.close()
            connection.close()
        else:
            message = 'Datenbankverbindung fehlgeschlagen!'
    
    return render_template('Login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('Benutzer_id', None)
    return render_template('Logout.html')

# REFACTORED - a_index
@app.route('/index')
def index():
    return render_template('index.html')

# REFACTORED - a_index
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/benutzer_verwaltung") # getestet: geht nicht
def benutzer_verwaltung():
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")
    myresult = cursor.fetchall()  # Gibt eine Liste von Tupeln zurück

    updated_result = []
    for row in myresult:
        user_list = list(row)  # Konvertiere das Tupel in eine Liste, damit es veränderbar ist
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

        connection = db_connection()
        cursor = connection.cursor()
        sql = "UPDATE user_data SET Benutzername = %s, Gruppe = %s, Rolle = %s WHERE Benutzer_id = %s"

        val = (name, gruppen_id, rolle, user_id)

        try:
            cursor.execute(sql, val)
            connection.commit()
            return benutzer_verwaltung()
        except Exception as e:
            connection.rollback()
            return f"Fehler: {str(e)}"
    return render_template("ticket_zuweisen.html")

@app.route('/ticket_ausgabe', methods=["GET", "POST"])
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

@app.route('/ticket_bearbeiten', methods=["GET", "POST"])    
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

if __name__ == '__main__':
    app.run(debug=True)
