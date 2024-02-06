# HTW-Noten-Grabber

## Disclaimer 

*Die Verwendung dieses Skripts erfolgt auf eigene Gefahr. Der Autor übernimmt keine Haftung für Schäden, die durch die Verwendung dieses Skripts entstehen.*

## Funktionen

Dieses Skript loggt sich in den Notenbereich der HTW Dresden ein und überprüft in regelmäßigen Abständen, ob es neue Noten gibt. Wenn neue Noten vorhanden sind, wird eine Pushbullet-Benachrichtigung gesendet.

Den Access-Token für Pushbullet könnt ihr, nachdem ihr euch einen Account angelegt habt, auf der [Pushbullet Website](https://www.pushbullet.com/#settings) unter `Settings > Account > Access Tokens` anlegen.

Die Funktionsweise des Skripts basiert auf der Struktur der HTW-Noten-Seite mit der Version **v2.0.2**.

Sollte es in naher Zukunft strukturänderungen an dieser Seite geben, könnte das Skript nicht mehr funktionieren.

## Setup & Installationsanleitung

1. Klone das Git-Repo auf den Zielsystem

    ```bash
    git clone git@github.com:MaxPtg/htwd-noten-checker.git
    ```

2. Lege eine `.env`-Datei im Stammverzeichnis des Projekts an und füge die folgenden Umgebungsvariablen hinzu:

    ```bash
    # HTWD Credentials
    HTWD_URL = "https://mobil.htw-dresden.de/de/mein-studium/noten-und-pruefungen" # default
    HTWD_USERNAME = "s*****" # s-Nummer
    HTWD_PASSWORD = "*********" # Passwort

    # Application Config
    POLL_INTERVAL = 600 # every x seconds
    POST_GRADES = "true" # or "false"

    # Pushbullet Credentials
    PUSHBULLET_ENABLED = "false" # or "true"
    PUSHBULLET_TOKEN = "o.*********"

    # Telegram Bot Credentials
    TELEGRAM_ENABLED = "false" # or "true"
    TELEGRAM_BOT_TOKEN = "**********:***********************"
    TELEGRAM_CHAT_ID = "-*********"
    ```

3. Installiere `docker` und `docker-compose` auf dem Zielsystem. Weitere Informationen zur Installation findest du in der offiziellen Docker-Dokumentation und deinem jeweiligen Zielsystem.

    ```bash
    sudo apt update -y && sudo apt upgrade -y
    sudo apt install docker docker-compose -y 
    ```

## Ausführung

Builde & starte den Docker-Container mit folgendem Befehl:

`docker-compose up --build -d`

Zugriff auf die Logs erhälst du mit folgendem Befehl:

`docker-compose logs -f`

## Bekannte Fehler

- Nahezu kein Error-Reporting
- Logging im Docker-Container funktioniert nicht richtig