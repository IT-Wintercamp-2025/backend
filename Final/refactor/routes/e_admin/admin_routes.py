from flask import render_template, Blueprint, request, session, redirect, url_for
import mysql.connector

# __name__ = "admin"
admin_blueprint = Blueprint("admin", __name__, template_folder="templates")

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

@admin_blueprint.route("/admin/user")
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


@admin_blueprint.route('/admin/dashboard')
def admin():
    return render_template('admin.html')

@admin_blueprint.route('/admin/lock_user')
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

@admin_blueprint.route('/admin/unlock_user')
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

@admin_blueprint.route('/admin/edit_user')
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

@admin_blueprint.route('/admin/execute_user_edit')
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

def register_routes(app):
    app.register_blueprint(admin_blueprint)
