# Fixture comparison – selbst hosten

## Dateien
- `index.html` – die fertige Webseite (das ist die Datei, die online geht)
- `template.html` – Design und Funktionen der Seite, ohne Daten
- `build.py` – erzeugt `index.html` neu aus deiner `FixtureDB.db`

## Daten aktualisieren
1. `FixtureDB.db` in denselben Ordner wie `build.py` legen.
2. Im Terminal in diesen Ordner wechseln und ausführen:
   `python build.py`   (auf dem Mac ggf. `python3 build.py`)
3. Die neue `index.html` auf GitHub hochladen und die alte ersetzen.
   Nach ein bis zwei Minuten ist die Seite aktualisiert.

Python gibt es kostenlos unter https://www.python.org/downloads/ – auf dem Mac ist es meist schon installiert.
