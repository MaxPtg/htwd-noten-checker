import time, requests, json, re, datetime, os, threading, random
from dotenv import load_dotenv
from bs4 import BeautifulSoup


"""
Author:     Max Patecky
Contact:    max.patecky@stud.htw-dresden.de

Script-Version:     1.0.0
HTWD-Mobil-Version: 2.0.3

First Release:  2023-07-30
Latest Update:  2024-01-21

Ich übernehme keine Haftung für Schäden, die durch die Verwendung dieses Skripts entstehen.
Jede Verwendung erfolgt auf eigene Gefahr.

Dieses Skript loggt sich in den Notenbereich der HTW Dresden ein und überprüft in regelmäßigen Abständen, ob es neue Noten gibt.
Wenn neue Noten vorhanden sind, wird eine Pushbullet-Benachrichtigung gesendet.

Die Funktionsweise des Skripts basiert auf der Struktur der HTW-Noten-Seite mit der oben angegebenen Version.
"""


load_dotenv()

HTWD_URL = "https://mobil.htw-dresden.de/de/mein-studium/noten-und-pruefungen"
PUSHBULLET_URL = "https://api.pushbullet.com/v2/pushes"
SLEEP_TIME = 600
LOG_DIR = "logs/"
LOG_FILE = "latest.log"


# prints message with timestamp and saves it to log file
def log(message, log_type="INFO"):
    timestamp = datetime.datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
    
    print(f"[{timestamp}] [{log_type}] {message}")
    
    with open(LOG_DIR + LOG_FILE, "a") as log_file:
        log_file.write(f"[{timestamp}] [{log_type}] {message}\n")


def send_pushbullet_notification(title, message):
    data = {
        'type': 'note',
        'title': title,
        'body': message
    }
    headers = {
        'Access-Token': os.getenv('PUSHBULLET_TOKEN'),
        'Content-Type': 'application/json'
    }
    response = requests.post(PUSHBULLET_URL, data=json.dumps(data), headers=headers)
    if response.status_code != 200:
        log("Pushbullet-Benachrichtigung konnte nicht gesendet werden!", "WARNING")
        log("Response-Code: " + str(response.status_code), "WARNING")
        

# Login to the grades page of HTW Dresden
def login(username, password):
    with requests.session() as session:
        payload = {
            '__referrer[@extension]': 'Felogin',
            '__referrer@controller]': 'Login',
            '__referrer@action]': 'login',
            '__referrerarguments]': 'YTowOnt952eec09e0e12541d15fc1a1e8438e551752590ed',
            '__referrer@request]': '{"@extension":"Felogin","@controller":"Login","@action":"login"}425cf7642bb3ecf60c6c7cb2e9befc2e0de384f7',
            '__trustedProperties': '{"user":1,"pass":1,"submit":1,"logintype":1,"pid":1,"noredirect":1}580eca94edf193692ce394cae2c2eeec5596c9b4',
            'user': username,
            'pass': password,
            'submit': 'Anmelden',
            'logintype': 'login',
            'pid': '21@968399d1618f39ccb731fc883946c1e11b5c6a9f'
        }
        response = session.post(HTWD_URL, data=payload)
        if response.status_code != 200:
            log("Login auf HTWD Mobil fehlgeschlagen!", "CRITICAL")
            return None
        return session


# Get the grades from the grades page of HTW Dresden
def get_current_grades(session):
    request = session.get(HTWD_URL).text
    html = BeautifulSoup(request, "html.parser")
    
    grade_elements = html.select('.align-items-baseline.collapsed.list-group-item.list-group-custom-item')
    grades_json = []
    
    for element in grade_elements:
        grade = element.select_one('span').text.strip()
        module = element.select_one('div > h4').text.strip()
        if not re.match(r'^\d+,\d+$', grade):
            continue
        grades_json.append({
            'grade': grade,
            'module': module,
        })
    return grades_json, len(grades_json)


# start grade checker thread
def run_grade_checker(username, password):
    log("Konfigurierter Benutzer: " + username, "INFO")
    
    while True:
        session = login(username, password)
        
        if session is not None:
            grades_json, grades_count = get_current_grades(session)
            
            global prev_grades_count
            global prev_grades_json
            
            if grades_count > prev_grades_count:
                # Filter out new grades
                new_grades = []
                for grade in grades_json:
                    if grade not in prev_grades_json:
                        new_grades.append(grade)
                
                # Update prev_grades_json and send pushbullet notification for each new grade
                if prev_grades_count > 0:
                    send_pushbullet_notification("HTWD Noten Checker", "Es gibt neue Noten!")
                    for grade in new_grades:
                        send_pushbullet_notification(grade['module'], "Note:" + grade['grade'])
                    
                # update prev_grades_count and prev_grades_json
                prev_grades_count = grades_count
                prev_grades_json = grades_json
            else:
                log("Keine neuen Noten! (" + str(grades_count) + " / " + str(prev_grades_count) + ")", "INFO")
                
                
        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    # create log dir in current directory if not exists
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)
    
    global prev_grades_count
    prev_grades_count = 0
    
    global prev_grades_json
    prev_grades_json = []
    
    thread = threading.Thread(
        target=run_grade_checker, 
        args=(
            os.getenv('HTWD_USERNAME'), 
            os.getenv('HTWD_PASSWORD'))
        )
    thread.start()
    
    log("HTWD Noten-Checker gestartet!", "INFO")
    
    timestamp = datetime.datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
    send_pushbullet_notification("HTWD Noten-Checker", "Der Noten-Checker wurde gestartet ("+timestamp+")!")

    try:
        while thread.is_alive():
            thread.join(1)
    except KeyboardInterrupt:
        thread._stop()
        log("HTWD Noten-Checker wurde ordentlich beendet.", "INFO")

    