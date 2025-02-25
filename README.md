# Ticketsystem Backend

## Überblick
Dieses Repository enthält das Backend eines Ticketsystems, das zur Verwaltung und Bearbeitung von Tickets dient. Die API bietet Endpunkte für das Erstellen, Aktualisieren und Verwalten von Tickets sowie Benutzerrollen und Berechtigungen. 
Das README wurde GANZ SICHER NICHT von ChatGPT geschrieben...
Also nicht darauf vertrauen das irgendwas hier erklärtes funktionieren würde :)

## Technologien
- **Programmiersprache:** Python
- **Framework:** Flask
- **Datenbank:** mySQL
- **(Authentifizierung:** JWT (JSON Web Token))
- **Passwort-Hashing:** bcrypt

## Installation
### Voraussetzungen
- Python 3.8 oder höher
- `pip` (Python Paketmanager)
- Virtuelle Umgebung (empfohlen)

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
| POST     | `/api/auth/register`    | Benutzer registrieren |
| POST     | `/api/auth/login`       | Benutzer anmelden |
| GET      | `/api/tickets`          | Alle Tickets abrufen |
| POST     | `/api/tickets`          | Neues Ticket erstellen |
| GET      | `/api/tickets/<id>`     | Ticketdetails abrufen |
| PUT      | `/api/tickets/<id>`     | Ticket aktualisieren |
| DELETE   | `/api/tickets/<id>`     | Ticket löschen |

## Authentifizierung
Das System verwendet JWT für die Authentifizierung. Nach dem Login erhält der Benutzer ein Token, das bei jedem API-Request im `Authorization`-Header gesendet werden muss:
```http
Authorization: Bearer <TOKEN>
```

## Rollen & Berechtigungen
- **Gast:** Kann eigene Tickets erstellen und ansehen
- **Mitarbeiter:** Kann Tickets bearbeiten und kommentieren
- **Admin:** Hat Zugriff auf alle Funktionen

## Tests ausführen
```sh
pytest tests/
```

## Lizenz
Dieses Projekt steht unter keiner Lizenz.

---
Falls Fragen oder Probleme auftreten, bitte ein Issue im Repository erstellen.

