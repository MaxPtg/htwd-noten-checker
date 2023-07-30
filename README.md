# HTW-Noten-Grabber

## Disclaimer 

*Die Verwendung dieses Skripts erfolgt auf eigene Gefahr. Der Autor übernimmt keine Haftung für Schäden, die durch die Verwendung dieses Skripts entstehen.*

## Funktionen

Dieses Skript loggt sich in den Notenbereich der HTW Dresden ein und überprüft in regelmäßigen Abständen, ob es neue Noten gibt. Wenn neue Noten vorhanden sind, wird eine Pushbullet-Benachrichtigung gesendet.

Die Funktionsweise des Skripts basiert auf der Struktur der HTW-Noten-Seite mit der Version **v2.0.2**.

Sollte es in naher Zukunft strukturänderungen an dieser Seite geben, könnte das Skript nicht mehr funktionieren.

## Setup & Installationsanleitung

Legen Sie eine `.env`-Datei im Stammverzeichnis des Projekts an und füge die folgenden Umgebungsvariablen hinzu:

```bash
# HTWD Credentials
HTWD_USERNAME = "s*****"
HTWD_PASSWORD = "*********"

# Pushbullet Credentials
PUSHBULLET_TOKEN = "o.*********"
```

Installiere Docker und Docker Compose auf dem Zielsystem. Weitere Informationen zur Installation findest du in der offiziellen Docker-Dokumentation und Docker Compose-Dokumentation.

## Ausführung

Builde & starte den Docker-Container mit folgendem Befehl:

`docker-compose up --build -d`

Zugriff auf die Logs erhälst du mit folgendem Befehl:

`docker-compose logs -f`

## Bekannte Fehler

- Nahezu kein Error-Reporting
- Logging im Docker-Container funktioniert nicht richtig