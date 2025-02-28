from flask import render_template, Blueprint, request, session, redirect, url_for
import mysql.connector

# __name__ = "user"
user_blueprint = Blueprint("user", __name__, template_folder="templates")

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

@user_blueprint.route('/user/test')
def user():
    return render_template('user.html')


def register_routes(app):
    app.register_blueprint(user_blueprint)
