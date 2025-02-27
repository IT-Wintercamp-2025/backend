import mysql.connector

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
    

# Flak Route: Anwendung/Voraussetzung
    """Voraussetzung:
    
    user_id = session('Benutzer_id')
        
        sql =  
        SELECT Gruppe
        FROM user_data
        WHERE Benutzer_id = %s 
        
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_id,)) 
        benutzer_team = cursor.fetchone()
        cursor.close()
        connection.close()

        if benutzer_team is None:
            return jsonify({"error": "Nutzerteam nicht gefunden"}), 404

        
        Verwendung:
        
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
        dictionary_status_2_erstelldatum_reverse_searched = ticket_manager.suche_im_dictionary("")"""