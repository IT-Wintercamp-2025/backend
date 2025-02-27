# Ticketsystem Backend

## Überblick
Ein vollständiges Ticketing-System mit Benutzerverwaltung, Rollenkonzept und MySQL-Integration.  
⚠️ **Achtung:** Dieses README wurde ZU 100% VON MENSCHEN geschrieben. Garantiert. Wirklich. 😉

## Features
- 🔐 Session-basierte Authentifizierung mit bcrypt
- 👥 Rollenbasierte Zugriffskontrolle (Admin/Mitarbeiter/Gast)
- 🎫 Ticket-Lebenszyklus-Verwaltung
- 📆 Sprint-Planungssystem
- 💬 Kommentarfunktion (Grundgerüst)
- 🛠️ Benutzersperrung & Rollenverwaltung

## Technologien
| Bereich         | Technologie               |
|-----------------|---------------------------|
| Backend         | Python 3 + Flask          |
| Datenbank       | MySQL/MariaDB             |
| Sicherheit      | bcrypt + parametrisierte Queries |
| Frontend        | Jinja2-Templates          |

## Datenbankstruktur
![DB-Schema](https://via.placeholder.com/800x500.png?text=DB-Schema+Diagramm)

### Kern-Tabellen
| Tabelle         | Beschreibung                     |
|-----------------|----------------------------------|
| `user_data`     | Benutzer + Login-Daten          |
| `ticket_data`   | Tickets mit Metadaten           |
| `gruppe`        | Teams (Frontend/Backend/Infra)  |
| `status`        | Ticket-Status (Neu/Bearbeitung/Erledigt) |
| `prio`          | Prioritätsstufen                |
| `sprint`        | 1-Wochen-Sprints bis 12/2025    |

### Beispiel-Daten
```sql
-- Sample Admin
INSERT INTO user_data VALUES (
  1, 
  'SuperAdmin', 
  'admin@system.de', 
  '$2b$12$...hashed...', 
  2,  -- Gruppe: Backend
  2,  -- Rolle: Admin
  0   -- Nicht gesperrt
);
```

## Installation
### Voraussetzungen
- Python 3.10+
- MariaDB/MySQL Server
- libmysqlclient-dev

### Setup
1. Datenbank erstellen:
```bash
mysql -u root -p -e "CREATE DATABASE Backend3"
```

2. Schema importieren:
```bash
mysql -u root -p Backend3 < backend(3).sql
```

3. Konfiguration anpassen (`app_full.py`):
```python
def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",      # 🚨 Nicht in Produktion!
        password="1234",  # 🚨 Niemals im Code hardcoden!
        database="Backend3"
    )
```

4. Abhängigkeiten installieren:
```bash
pip install flask mysql-connector-python bcrypt
```

5. Server starten:
```bash
python app_full.py
```

## API-Endpunkte
| Endpoint                 | Methoden | Zugriff      | Beschreibung                |
|--------------------------|----------|--------------|----------------------------|
| `/SignUp`                | GET/POST | Public       | Benutzerregistrierung       |
| `/benutzer_verwaltung`   | GET      | Nur Admin    | Benutzerliste mit Filtern   |
| `/ticket_ausgabe`        | GET      | Alle Rollen  | Ticket-Detailansicht        |
| `/sprint/{id}`           | GET      | Mitarbeiter+ | Sprint-Planungsansicht      |

## Sicherheit
- 🛡️ **Passwörter:** bcrypt mit 12 Runden Salt
- 🕵️ **Sessions:** Flask-Secret-Key + Cookie-Hashing
- 🚫 **SQL-Injection:** Sämtliche Queries parametrisiert
- 🔒 **Lockout:** Gesperrte Benutzer (außer Admins) können sich nicht anmelden

## Rollenkonzept
| Rolle        | Rechte                     | DB-Wert |
|--------------|----------------------------|---------|
| **Gast**     | Ticket erstellen/lesen     | 0       |
| **Mitarbeiter**| Tickets bearbeiten       | 1       |
| **Admin**    | Vollzugriff + Sperrung     | 2       |

## Known Issues
- 🗓️ Datumsformat inkonsistent (ISO vs DD.MM.YYYY)
- 📝 Kommentarfunktion noch nicht implementiert
- 🔗 Fehlende Foreign Keys in einigen Tabellen

## Lizenz
Public Domain - Nutzung auf eigene Gefahr.  
⚠️ Enthält absichtliche Sicherheitslücken für Schulungszwecke!

---

**Tipp:** Für Produktionsnutzung unbedingt:
1. Secret-Key ändern (`app.secret_key`)
2. Datenbank-Passwort durch Umgebungsvariablen ersetzen
3. SSL/TLS für MySQL-Verbindung aktivieren
