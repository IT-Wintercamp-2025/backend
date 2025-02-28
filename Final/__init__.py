import mysql
from flask import Flask

from Final.refactor.routes.a_index import index_routes


# TODO: Insert correct database credentials
# TODO #2: Let database import .sql file -> docker-compose.yml of application-dockerized
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
    app = Flask(__name__)
    app.secret_key = '0229'

    index_routes.register_routes(app)
    print("Routes registered")

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
