Anleitung - Wie geht es jetzt weiter?

- Der Startpunkt der Anwendung ist die [__init__.py](https://github.com/IT-Wintercamp-2025/backend/blob/main/Final/__init__.py)
- Die __init__.py ist dafür verantwortlich, alle URLs für den Browser zu registrieren, sie also verfügbar zu machen.
- Lest euch bitte unbedingt die Kommentare in den create_app & register_blueprint_routes Methoden durch!

Diese Methode sorgt dafür, dass die bereitgestellten Dateien in Final/static und Final/refactor/routes geladen werden können.

```python
def register_blueprint_routes(app):
    index_routes.register_routes(app)
```

Eure Aufgabe besteht nun darin, die gegebene Struktur beizubehalten und darin den existierenden Code zu integrieren. <br>
Tipp: Habt ihr zu einer Route mehrere Dateien? Nehmt euch ein Beispiel an den, in den Dateien ganz oben befindlichen "from" und "import"
keywords und wie diese aufgebaut sind. Damit könnte ihr die Dateien verkleinern und so die Wartbarkeit sowie Benutzerfreundlichkeit
sicherstellen. 
