# Ticketsystem Backend

## Überblick
Dieses Repository enthält das Backend eines Ticketsystems, das zur Verwaltung und Bearbeitung von Tickets dient. Die API bietet Endpunkte für das Erstellen, Aktualisieren und Verwalten von Tickets sowie Benutzerrollen und Berechtigungen. 
Das README wurde GANZ SICHER NICHT von ChatGPT geschrieben...
Also nicht darauf vertrauen das irgendwas hier erklärtes funktionieren würde :)

## Technologien
- **Programmiersprache:** Python 3
- **Framework:** Flask
- **Datenbank:** MySQL
- **Authentifizierung:** Session-basiert mit bcrypt-Hashing
- **Frontend:** HTML/CSS

## Installation
### Voraussetzungen
- Python 3.8+
- MySQL Server
- Docker (optional, für lokale DB-Verbindung)

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
   venv\Scripts\activate  # Windows
   ```
3. Abhängigkeiten installieren:
   ```sh
   pip install -r requirements.txt
   ```
4. Umgebungsvariablen setzen:
   Erstelle eine `.env`-Datei und definiere Variablen wie:
   ```ini
   FLASK_ENV=development
   SECRET_KEY=geheime_schluessel
   DATABASE_URL=sqlite:///ticketsystem.db
   ```
5. Datenbank migrieren und initialisieren:
   ```sh
   flask db upgrade
   ```
6. Server starten:
   ```sh
   flask run
   ```

## API-Endpunkte
| Methode  | Endpunkt               | Beschreibung |
|----------|------------------------|--------------|
| POST     | `/auth/register`    | Benutzer registrieren |
| POST     | `/auth/login`       | Benutzer anmelden |
|          |                     | Dashboard         |
|          |                     | Ticket erstellung |
|          |                     | Ticketdetails abrufen|


## Sicherheit

- Passwörter werden mit bcrypt gehasht
- SQL-Injection Schutz durch parametrisierte Queries
- Session-Management mit Flask-Secret-Key

## Rollen & Berechtigungen
- ### Gast: Kann eigene Tickets erstellen und ansehen
- user_id = 0
- ### Mitarbeiter: Kann Tickets bearbeiten und kommentieren
- user_id = 1
- ### Admin: Hat Zugriff auf alle Funktionen
- user_id = 2


## Lizenz
Dieses Projekt steht unter keiner Lizenz.

---
Falls Fragen oder Probleme auftreten, bitte ein Issue im Repository erstellen.

