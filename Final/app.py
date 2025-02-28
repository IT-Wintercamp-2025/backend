import mysql
from flask import Flask

from refactor.routes.a_index import index_routes

app = Flask(__name__)

"""
An dieser Stelle müssen die Anmeldedaten der ticketsystem-database-1 angegeben werden.
Versucht möglichst, eine zentrale database_connection zu haben, da jeder Request eine neue Verbindung aufbauen muss.
    Das könnte die Leistung und Funktionstüchtigkeit beeinträchtigen.

TODO: Insert correct database credentials
TODO #2: Let database import .sql file -> docker-compose.yml of application-dockerized
"""


def database_connection():
    try:
        connection = mysql.connector.connect(
            host="ticketsystem-database-1",
            user="root",
            password="1234",
            database="backend"
        )
        return connection
    except mysql.connector.Error as error:
        print("Fehler bei der Datenbankverbindung:", error)
        return None


def create_app():
    app.secret_key = '0229'

    # Hier wird die lokale Methode register_blueprint_routes() aufgerufen, welche nacheinander alle HTML Seiten registriert
    register_blueprint_routes(app)
    print("Routes registered")


def register_blueprint_routes(app):
    """
    Der Aufruf index_routes.register_routes(app) ist ein Muster, anhand welchem ihr euch orientieren sollt.
    Ein Aufruf fasst sinnvoll gruppierbare Routen in einer Datei zusammen. Eine Ordner- und Dateistruktur habe ich AB Final/refactor/routes bereitgestellt.
        -> Hinweis: Die statischen Dateien wie style.css, Bilder, etc. befinden sich unter Final/static. Auch dort ist eine Ordner- und Dateistruktur gegeben.

        Führt die Muster und Beispiele sinnvoll fort, dann habt ihr einen super Überblick und könnt strukturiert das Projekt beenden.
    """

    """
    <gruppen_name(bspw. auth, user, ticket, admin)>_routes.register_routes(app)
    auth würde beispielsweise register, login und logout implementieren,
    user das anlegen, löschen, bearbeiten
    ticket "  
    """
    # Ihr müsst nichts weiter tun, als die untenliegende Zeile Code sinnvoll an die weiteren gruppierbaren HTML Seiten anzupassen und unter diesem Aufruf einzufügen - wieder und wieder. :)
    index_routes.register_routes(app)


if __name__ == '__main__':
    create_app()
    app.run(host='0.0.0.0', port=5000)
