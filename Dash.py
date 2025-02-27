@app.route("/dashboard", methods=["GET", "POST"])
def dashboard_show():
    tickets = []
    message = ""

    try:
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Ticket") 
        tickets = cursor.fetchall()
    except Exception as e:
        message = f"Fehler: {e}"
    finally:
        cursor.close()
        connection.close()

    return render_template("main.html", message=message, tickets=tickets)