from flask import Flask, render_template, request
import mysql.connector
import traceback

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
        print(f"Fehler1: {err}")
        return None

@app.route('/', methods=['GET', 'POST'])
def hello():#spaeter auch besserer name
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '', type=str)

    try:
        connection = db_connection()
        if connection is None:
            return "Fehler bei der Verbindung zur Datenbank."

        cursor = connection.cursor()

        search_filter = f"%{search_query}%"
        cursor.execute("""SELECT COUNT(*) FROM user_data WHERE Benutzername LIKE %s OR Email LIKE %s OR Gruppe LIKE %s""", (search_filter, search_filter, search_filter))

        total_rows = cursor.fetchone()[0]
        rows_per_page = 10
        offset = (page - 1) * rows_per_page
        total_pages = (total_rows + rows_per_page - 1) / rows_per_page

        cursor.execute("""SELECT * FROM user_data WHERE Benutzername LIKE %s OR Email LIKE %s OR Gruppe LIKE %s LIMIT %s OFFSET %s""", (search_filter, search_filter, search_filter, rows_per_page, offset))

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('benutzerliste.html', myresult=results, search_query=search_query, total_pages=total_pages, current_page=page, total_rows=total_rows)

    except Exception as e:
        traceback.print_exc()
        return f"Fehler2: {e}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

@app.route('/benutzerliste.html', methods=['GET', 'POST'])
def benutzer_sperren():
    print("sperren")

@app.route('/benutzerliste.html', methods=['GET', 'POST'])
def benutzer_entsperren():
    print("entsperren")

@app.route('/benutzerliste.html', methods=['GET', 'POST'])
def benutzer_bearbeiten():
    print("bearbeiten")
