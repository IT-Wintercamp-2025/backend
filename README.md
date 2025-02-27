```markdown
# Ticketsystem Backend

## Überblick
Dieses Repository enthält das Backend eines Ticketsystems zur Verwaltung von Benutzern und Tickets. Es bietet Funktionen für Registrierung, Authentifizierung, Benutzerverwaltung und Ticketbearbeitung mit rollenbasiertem Zugriff.

## Technologien
- **Programmiersprache:** Python 3
- **Framework:** Flask
- **Datenbank:** MySQL
- **Authentifizierung:** Session-basiert mit bcrypt-Hashing
- **Frontend:** HTML-Templates (Jinja2)

## Installation
### Voraussetzungen
- Python 3.8+
- MySQL Server
- `mysql-connector-python`, `flask`, `bcrypt` (siehe `requirements.txt`)

### Setup-Anleitung
1. Repository klonen:
   ```sh
   git clone <REPOSITORY_URL>
   cd ticketsystem-backend
   ```

2. Virtuelle Umgebung erstellen und aktivieren:
   ```sh
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. Abhängigkeiten installieren:
   ```sh
   pip install -r requirements.txt
   ```

4. MySQL-Datenbank einrichten:
   - Datenbank namens `Backend3` erstellen.
   - Tabellen `user_data`, `gruppe`, `status`, `prio`, und `ticket_data` importieren (Schema aus dem Code entnehmen).

5. Konfiguration anpassen:
   - In `app_full.py` die Datenbankverbindung prüfen (`host`, `user`, `password`).
   - Geheimen Schlüssel (`app.secret_key`) für Produktionsumgebungen ändern.

6. Server starten:
   ```sh
   python app_full.py
   ```

## API-Endpunkte
| Methode  | Endpunkt                   | Beschreibung                                  |
|----------|----------------------------|-----------------------------------------------|
| GET/POST | `/SignUp`                  | Benutzerregistrierung                         |
| GET/POST | `/login`                   | Benutzeranmeldung                             |
| GET      | `/logout`                  | Session beenden                               |
| GET      | `/benutzer_verwaltung`     | Liste aller Benutzer anzeigen                 |
| POST     | `/benutzer_sperren`        | Benutzer sperren                              |
| POST     | `/benutzer_entsperren`     | Benutzer entsperren                           |
| GET/POST | `/benutzer_bearbeiten`     | Benutzerdaten bearbeiten                      |
| POST     | `/benutzer_bearbeiten_exe` | Speichern der Benutzeränderungen              |
| GET      | `/ticket_ausgabe`          | Ticketdetails anzeigen (Beispiel-Ticket-ID)   |
| POST     | `/ticket_bearbeiten`       | Ticket aktualisieren                          |

## Sicherheit
- **Passwort-Hashing:** BCrypt mit Salt-Generierung.
- **SQL-Injection-Schutz:** Parametrisierte Queries.
- **Session-Management:** Flask-Sessions mit Secret-Key (Im Produktivbetrieb ersetzen!).
- **Validierung:** Benutzername/Passwort-Prüfung (Länge, Zeichen).

## Rollen & Berechtigungen
| Rolle      | `Rolle`-Wert | Berechtigungen                                  |
|------------|--------------|-------------------------------------------------|
| **Admin**  | 2            | Vollzugriff (Benutzer sperren, Rollen verwalten)|
| **Mitarbeiter** | 1       | Tickets bearbeiten, Kommentare hinzufügen       |
| **Gast**   | 0            | Eigene Tickets erstellen/ansehen                |

## Datenbankstruktur (Auszug)
- **user_data:**  
  `Benutzer_id`, `Benutzername`, `Passwort`, `Gruppe`, `Rolle`, `Sperren`
- **ticket_data:**  
  `Ticket_id`, `Betreff`, `Beschreibung`, `Erstelldatum`, `Status`, `Prio`, `Team`

## Lizenz
Dieses Projekt steht unter keiner Lizenz. Nutzung auf eigene Verantwortung.

---
**Hinweis:**  
- Testdaten im Code (z. B. `ticket_id = 3`) müssen im Frontend dynamisch ersetzt werden.
- Bei Fehlern: Prüfen Sie die Konsolenausgaben und Datenbankverbindungen.
```
