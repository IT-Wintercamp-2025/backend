from flask import Flask, session, render_template, redirect, request, url_for
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = '0815'

def db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="Backend"
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

            hashed_passwort = bcrypt.hashpw(passwort.encode("utf-8"), bcrypt.gensalt())
            cursor.execute("INSERT INTO user_data (Benutzername, Passwort, Email) VALUES (%s, %s, %s)", (username, hashed_passwort, username+"@Email.com"))
            connection.commit()
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

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
