from flask import Flask, jsonify, render_template, request, session
import mysql.connector

app = Flask(__name__)

def db_connection():
    try:
        connection = mysql.connector.connect(
            host="host.docker.internal",
            user="root",
            password="1234",
            database="backend"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Fehler: {err}")
        return None
    
class TicketManager:
    def __init__(self, benutzer_team):
        self.dictionary_status_2_erstelldatum_reverse_searched = {}
        self.benutzer_team = benutzer_team

    def erstellung_dictionary_gesamt(self):
        sql = """
        SELECT Ticket_id, Betreff 
        FROM ticket_data
        WHERE Team = %s  
        ORDER BY Erstelldatum DESC
        """
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (self.benutzer_team,)) 
        tickets = cursor.fetchall()
        cursor.close()
        connection.close()

        dictionary_gesamt = {ticket[0]: ticket[1] for ticket in tickets}
        return dictionary_gesamt

    def dictionary_by_status_erstelldatum(self, status):
        sql = """
        SELECT Ticket_id, Betreff 
        FROM ticket_data 
        WHERE Team = %s AND Status = %s
        ORDER BY Erstelldatum ASC
        """
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (self.benutzer_team, status))
        tickets = cursor.fetchall()
        cursor.close()
        connection.close()

        dictionary = {ticket[0]: ticket[1] for ticket in tickets}
        return dictionary

    def dictionary_status_0_erstelldatum(self):
        return self.dictionary_by_status_erstelldatum(0)

    def dictionary_status_1_erstelldatum(self):
        return self.dictionary_by_status_erstelldatum(1)
    
    def dictionary_by_status_erstelldatum_reverse(self, status):
        sql = """
        SELECT Ticket_id, Betreff 
        FROM ticket_data 
        WHERE Team = %s AND Status = %s
        ORDER BY Erstelldatum DESC
        """
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (self.benutzer_team, status))
        tickets = cursor.fetchall()
        cursor.close()
        connection.close()

        dictionary = {ticket[0]: ticket[1] for ticket in tickets}
        return dictionary

    def dictionary_status_2_erstelldatum_reverse(self):
        return self.dictionary_by_status_erstelldatum_reverse(2)
    
    def dictionary_by_status_ablaufdatum(self, status):
        sql = """
        SELECT Ticket_id, Betreff 
        FROM ticket_data 
        WHERE Team = %s AND Status = %s
        ORDER BY sprint ASC
        """
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (self.benutzer_team, status))
        tickets = cursor.fetchall()
        cursor.close()
        connection.close()

        dictionary = {ticket[0]: ticket[1] for ticket in tickets}
        return dictionary

    def dictionary_status_0_ablaufdatum(self):
        return self.dictionary_by_status_ablaufdatum(0)

    def dictionary_status_1_ablaufdatum(self):
        return self.dictionary_by_status_ablaufdatum(1)
    
    def dictionary_by_status_prio(self, status):
        sql = """
        SELECT Ticket_id, Betreff 
        FROM ticket_data 
        WHERE Team = %s AND Status = %s
        ORDER BY prio ASC
        """
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (self.benutzer_team, status))
        tickets = cursor.fetchall()
        cursor.close()
        connection.close()

        dictionary = {ticket[0]: ticket[1] for ticket in tickets}
        return dictionary

    def dictionary_status_0_prio(self):
        return self.dictionary_by_status_prio(0)

    def dictionary_status_1_prio(self):
        return self.dictionary_by_status_prio(1)

    def suche_im_dictionary(self, suchbegriff):
        for ticked_id, betreff in self.dictionary_status_2_erstelldatum_reverse().items():
            if suchbegriff.lower() in betreff.lower():  # Fallunabhängige Suche
                self.dictionary_status_2_erstelldatum_reverse_searched[ticked_id] = betreff
        
        return self.dictionary_status_2_erstelldatum_reverse_searched

@app.route("/Ticket_Uebersicht", methods = ["GET", "POST"])
def dashboard():
    ticket = []
    try:

        user_id = session('Benutzer_id')
        
        sql =  """
        SELECT Gruppe
        FROM user_data
        WHERE Benutzer_id = %s 
        """
        
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_id,)) 
        benutzer_team = cursor.fetchone()
        cursor.close()
        connection.close()

        if benutzer_team is None:
            return jsonify({"error": "Nutzerteam nicht gefunden"}), 404

        ticket_manager = TicketManager(benutzer_team[0])

        # Gesamt-Dictionary mit Ticket-IDs und Betreffs
        dictionary_gesamt = ticket_manager.erstellung_dictionary_gesamt()

        # Status-Dictionaries erstellen mit methoden aus klasse ticket_manager
        dictionary_status_0_erstelldatum = ticket_manager.dictionary_status_0_erstelldatum()
        dictionary_status_0_ablaufdatum = ticket_manager.dictionary_status_0_ablaufdatum()
        dictionary_status_0_prio = ticket_manager.dictionary_status_0_prio()
        dictionary_status_1_erstelldatum = ticket_manager.dictionary_status_1_erstelldatum()
        dictionary_status_1_ablaufdatum = ticket_manager.dictionary_status_1_ablaufdatum()
        dictionary_status_1_prio = ticket_manager.dictionary_status_1_prio()
        dictionary_status_2_erstelldatum_reverse = ticket_manager.dictionary_status_2_erstelldatum_reverse()
        dictionary_status_2_erstelldatum_reverse_searched = ticket_manager.suche_im_dictionary("")


        ausgewaltes_dict = {}
        status_filter0 = request.form.get('status0')
        status_filter1 = request.form.get('status1')
        status_filter2 = request.form.get('status2')

        if status_filter0 == "Erstelldatum":
            ausgewaltes_dict = dictionary_status_0_erstelldatum
        if status_filter0 == "Ablaufdatum":
            ausgewaltes_dict = dictionary_status_0_ablaufdatum
        if status_filter0 == "Priorität":
            ausgewaltes_dict = dictionary_status_0_prio
        
        if status_filter1 == "Erstelldatum":
            ausgewaltes_dict = dictionary_status_1_erstelldatum
        if status_filter1 == "Ablaufdatum":
            ausgewaltes_dict = dictionary_status_1_ablaufdatum
        if status_filter1 == "Priorität":
            ausgewaltes_dict = dictionary_status_1_prio

        if status_filter2 == "normal":
            ausgewaltes_dict = dictionary_status_2_erstelldatum_reverse

        query = """
        SELECT ticket_data.Ticket_id, user_data.Benutzername, ticket_data.Betreff, ticket_data.Beschreibung, ticket_data.Status, ticket_data.Prio, ticket_data.Team, ticket_data.Erstelldatum, ticket_data.Sprint
        FROM ticket_data
        INNER JOIN user_data
        ON ticket_data.Benutzer_id = user_data.Benutzer_id
        WHERE ticket_data.Ticket_id = %s;  -- Platzhalter für TicketID
        """

        connection = db_connection()
        cursor = connection.cursor()

        for ticket_id in ausgewaltes_dict.keys():
            cursor.execute(query, (ticket_id,))
            ticket = cursor.fetchone()
    

    finally: 
        cursor.close()
        connection.close()

        return render_template("Ticket_Uebersicht.html", ticket=ticket)
    
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)