## Super, du hast es gefunden. Wie geht es jetzt weiter?

- Der Startpunkt der Anwendung ist nun final die [__init__.py](https://github.com/IT-Wintercamp-2025/backend/blob/main/Final/__init__.py) Datei in /Final
- Die __init__.py ist dafür verantwortlich, alle möglichen URLs für den Browser zu registrieren.
- Lest euch bitte unbedingt die Kommentare in der create_app & register_blueprint_routes Methode durch!
- Die Routen befinden sich in sortierbaren Ordnern - ermöglich wird das durch einen aufsteigenden Prefix wie "a_", "b_", ..., "z_"
    - Versucht, sie in einer logischen und untereinaner zusammenhängenden Reihenfolge anzuordnen :) 

Diese Methoden sorgen dafür, dass die bereitgestellten Dateien in Final/static und Final/refactor/routes geladen und verwendet werden können.<br>
Diese Methode ist die wichtigste. Sie registriert die eigentlichen Routen. 
```python
def register_blueprint_routes(app):
    index_routes.register_routes(app)
```

Eure Aufgabe besteht nun darin, die gegebene Struktur beizubehalten und darin den existierenden Code zu integrieren. <br> <br>
Tipp: Habt ihr zu einer Route mehrere logisch zusammenängende Dateien? (Bitte versucht genau das zu tun, damit wird es übersichtlicher und viel leichter!) Nehmt euch ein Beispiel an den, in den Dateien ganz oben befindlichen "from" und "import"
keywords und wie diese aufgebaut sind. Damit könnte ihr die Dateien verkleinern und so die Wartbarkeit sowie Benutzerfreundlichkeit
sicherstellen. Alle Dateien gehören dann in den jeweiligen Ordner der Route.
