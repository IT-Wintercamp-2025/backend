# Ticketsystem Backend

> [!CAUTION]
> DAS REPOSITORY WURDE FÜR FREITAG ÜBER NACHT TEILWEISE MIT PRODUKTIVEM BEISPIELCODE AUSGESTATTET.<br>
> BITTE VORERST NICHTS AUF GITHUB COMMITTEN ODER PUSHEN, BIS WEITERE ANWEISUNGEN ERFOLGEN.<br>
> SCHAUT UNBEDINGT IN DIESE [README.md](https://github.com/IT-Wintercamp-2025/backend/blob/main/Final/README.md)

## Übersicht

Ein vollständiges Ticketing-System zur Verwaltung von Benutzern, Tickets und Teamworkflows. Das System ermöglicht rollenbasierten Zugriff,
Ticketlebenszyklusverwaltung und Integration mit einer MySQL-Datenbank.

---

## Funktionen

- **Benutzerverwaltung**: Registrierung, Anmeldung, Sperrung und Rollenzuweisung.
- **Ticketmanagement**: Erstellung, Bearbeitung, Statusverfolgung und Priorisierung von Tickets.
- **Rollenbasierte Zugriffskontrolle**: Unterscheidung zwischen Admins, Mitarbeitern und Gästen.
- **Sprintplanung**: Zuordnung von Tickets zu Entwicklungs-Sprints.
- **Kommentarsystem**: Grundgerüst für Ticketkommentare (in Entwicklung).

---

## Technologien

| Komponente        | Technologie   | Version    |
|-------------------|---------------|------------|
| Backend-Framework | Flask         | 2.0.x      |
| Datenbank         | MySQL/MariaDB | 10.2+      |
| Passwort-Hashing  | bcrypt        | 4.0.x      |
| Templating-Engine | Jinja2        | 3.0.x      |
| API-Handling      | Flask-RESTful | Integriert |

---

## Installation

### Voraussetzungen

- **Python**: 3.10 oder höher
- **MySQL/MariaDB**: Laufender Server mit Zugangsdaten
- **Bibliotheken**: Siehe `requirements.txt`

### Schritt-für-Schritt-Anleitung

1. **Repository klonen**:
   ```bash
   git clone https://github.com/beispiel/ticketsystem-backend.git
   cd ticketsystem-backend
   ```

2. **Virtuelle Umgebung einrichten**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Abhängigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Datenbank konfigurieren**:
    - Datenbank erstellen:
      ```sql
      CREATE DATABASE Backend3 CHARACTER SET utf8 COLLATE utf8_unicode_ci;
      ```
    - Schema importieren:
      ```bash
      mysql -u <benutzer> -p Backend3 < backend(3).sql
      ```

5. **Konfigurationsdatei anpassen**:
    - In `app_full.py` die Datenbankverbindung aktualisieren:
      ```python
      def db_connection():
          return mysql.connector.connect(
              host="localhost",
              user="root",         # Durch Umgebungsvariable ersetzen
              password="sicheres_passwort",
              database="Backend3"
          )
      ```

6. **Server starten**:
   ```bash
   python app_full.py
   ```

---

## API-Dokumentation

### Benutzerendpunkte

| Endpoint               | Methode | Parameter (JSON-Body)                 | Beschreibung                        |
|------------------------|---------|---------------------------------------|-------------------------------------|
| `/SignUp`              | POST    | `username`, `password`, `password_be` | Registrierung eines neuen Benutzers |
| `/login`               | POST    | `username`, `password`                | Anmeldung und Session-Erstellung    |
| `/logout`              | GET     | -                                     | Session beenden                     |
| `/benutzer_verwaltung` | GET     | -                                     | Liste aller Benutzer (nur Admin)    |

### Ticketendpunkte

| Endpoint             | Methode | Parameter (JSON-Body)         | Beschreibung                |
|----------------------|---------|-------------------------------|-----------------------------|
| `/ticket_ausgabe`    | GET     | `ticket_id` (URL-Parameter)   | Detailansicht eines Tickets |
| `/ticket_bearbeiten` | POST    | `betreff_e`, `beschreibung_e` | Ticket aktualisieren        |

### Beispielaufruf

**Registrierung**:

```bash
curl -X POST http://localhost:5000/SignUp \
  -H "Content-Type: application/json" \
  -d '{"username": "max", "password": "geheim", "password_be": "geheim"}'
```

**Antwort**:

```json
{
  "message": "Registrierung erfolgreich!",
  "user_id": 3
}
```

---

## Datenbankschema

### Tabellenübersicht

| Tabelle       | Beschreibung                              |
|---------------|-------------------------------------------|
| `user_data`   | Benutzerkonten mit Passwörtern (bcrypt)   |
| `ticket_data` | Tickets mit Status, Priorität und Team    |
| `gruppe`      | Teams (z.B. Frontend, Backend)            |
| `status`      | Ticketstatus (Neu, Bearbeitung, Erledigt) |
| `prio`        | Prioritätsstufen (Niedrig, Mittel, Hoch)  |
| `sprint`      | Sprintzeiträume für Agile Planung         |

### Beziehungen

- **Tickets ↔ Benutzer**: Ein Benutzer (`user_data.Benutzer_id`) erstellt mehrere Tickets (`ticket_data.Benutzer_id`).
- **Tickets ↔ Gruppen**: Jedes Ticket ist einem Team (`gruppe.Gruppen_id`) zugewiesen.
- **Tickets ↔ Sprints**: Optionale Zuordnung zu Entwicklungs-Sprints (`sprint.Sprint_id`).

---

## Sicherheit

- **Passwörter**:
    - Hashing mit bcrypt und Salt-Generierung (12 Runden).
    - Beispiel: `hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())`.

- **SQL-Injection-Schutz**:
    - Alle Abfragen verwenden parametrisierte Statements:
      ```python
      cursor.execute("SELECT * FROM user_data WHERE Benutzername = %s", (username,))
      ```

- **Session-Management**:
    - Flask-Sessions mit signierten Cookies.
    - Session-Daten: `loggedin`, `Benutzer_id`, `Rolle`.

---

## Rollen und Berechtigungen

| Rolle           | Rechte                                                                         | DB-Wert |
|-----------------|--------------------------------------------------------------------------------|---------|
| **Gast**        | - Tickets erstellen/ansehen                                                    | 0       |
| **Mitarbeiter** | - Tickets bearbeiten<br>- Kommentare hinzufügen                                | 1       |
| **Admin**       | - Benutzer sperren/entsperren<br>- Rollen verwalten<br>- Alle Tickets anzeigen | 2       |

---

## Bekannte Probleme und TODO

- **Datenbank**:
    - Fehlende Foreign Key Constraints (z.B. `ticket_data.Team` → `gruppe.Gruppen_id`).
    - Inconsistent Datumsformate (`ticket_data.Erstelldatum` als String).

- **API**:
    - Keine Paginierung für `/benutzer_verwaltung`.
    - Kommentarfunktion (`/kommentar`) noch nicht implementiert.

---

## Lizenz

MIT-Lizenz. Einzelheiten finden Sie in der [LICENSE](LICENSE)-Datei.

---

## Beitragende

1. Forken Sie das Repository.
2. Erstellen Sie einen Feature-Branch: `git checkout -b feature/mein-feature`.
3. Committen Sie Ihre Änderungen: `git commit -m 'Hinzufügen: Awesome Feature'`.
4. Pushen Sie den Branch: `git push origin feature/mein-feature`.
5. Öffnen Sie einen Pull Request.

---

## Kontakt

Bei Fragen oder Problemen wenden Sie sich an [support@ticketsystem.de](mailto:support@ticketsystem.de) oder erstellen Sie ein Issue im
GitHub-Repository.
