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
            database="Backend2"
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
            gruppe = None

            hashed_passwort = bcrypt.hashpw(passwort.encode("utf-8"), bcrypt.gensalt())

            cursor.execute(
                "INSERT INTO user_data (Benutzername, Passwort, Email, Gruppe, Rolle) VALUES (%s, %s, %s, %s, %s)",
                (username, hashed_passwort, username + "@email.com", gruppe, rolle)
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

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
