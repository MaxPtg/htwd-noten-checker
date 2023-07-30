import time, requests, json, re, datetime, os, threading, random
from dotenv import load_dotenv
from bs4 import BeautifulSoup


"""
Author:     Max Patecky
Contact:    max.patecky@stud.htw-dresden.de

Script-Version:     1.0.0
HTWD-Mobil-Version: 2.0.2

First Release:  2023-07-30
Latest Update:  2023-07-30

Ich übernehme keine Haftung für Schäden, die durch die Verwendung dieses Skripts entstehen.
Jede Verwendung erfolgt auf eigene Gefahr.

Dieses Skript loggt sich in den Notenbereich der HTW Dresden ein und überprüft in regelmäßigen Abständen, ob es neue Noten gibt.
Wenn neue Noten vorhanden sind, wird eine Pushbullet-Benachrichtigung gesendet.

Die Funktionsweise des Skripts basiert auf der Struktur der HTW-Noten-Seite mit der Version v2.0.2. 
"""


load_dotenv()

HTWD_URL = "https://mobil.htw-dresden.de/de/mein-studium/noten-und-pruefungen"
PUSHBULLET_URL = "https://api.pushbullet.com/v2/pushes"
SLEEP_TIME = 600


def send_pushbullet_notification(title, message, timestamp):
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
        print("["+timestamp+"] >>> Benachrichtigung konnte nicht gesendet werden!")
        

# Login to the grades page of HTW Dresden
def login(username, password, timestamp):
    with requests.session() as s:
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
        response = s.post(HTWD_URL, data=payload)
        if response.status_code != 200:
            print("["+timestamp+"] >>> Login fehlgeschlagen!")
            return None
        return s


# Get the grades from the grades page of HTW Dresden
def get_current_grades(s):
    request = s.get(HTWD_URL).text
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


def run_grabber(username, password):
    print(">>> Starte grade_grabber für " + username + " ...")
    
    while True:
        timestamp = datetime.datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
        
        s = login(username, password, timestamp)
        
        if s is not None:
            grades_json, grades_count = get_current_grades(s)
            
            global prev_grades_count
            global prev_grades_json
            
            """ Tests
            print("1. Aktuelle Noten: " + str(grades_count))
            print("1. Vorherige Noten: " + str(prev_grades_count))
            
            if prev_grades_count > 0:
                print("appending random grades on 2nd run ...")
                grades_json.append({
                    'grade': str(random.randint(1, 5)) + "," + str(random.randint(0, 9)),
                    'module': "Testmodul"
                })
                grades_json.append({
                    'grade': str(random.randint(1, 5)) + "," + str(random.randint(0, 9)),
                    'module': "Testmodul"
                })
                grades_json.append({
                    'grade': str(random.randint(1, 5)) + "," + str(random.randint(0, 9)),
                    'module': "Testmodul"
                })
                grades_count += 3
                
            print("2. Aktuelle Noten: " + str(grades_count))
            print("2. Vorherige Noten: " + str(prev_grades_count))
            """
            
            if grades_count != prev_grades_count:
                # Filter out new grades
                new_grades = []
                for grade in grades_json:
                    if grade not in prev_grades_json:
                        new_grades.append(grade)
                
                # Update prev_grades_json and send pushbullet notification for each new grade
                if prev_grades_count > 0:
                    send_pushbullet_notification("HTWD Noten Checker", "Es gibt neue Noten!", timestamp)
                    for grade in new_grades:
                        send_pushbullet_notification(grade['module'], "Note:" + grade['grade'], timestamp)
                        
                prev_grades_count = grades_count
                prev_grades_json = grades_json
            #else:
                #print("["+timestamp+"] >>> Keine neuen Noten!")
                
        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    global prev_grades_count
    prev_grades_count = 0
    
    global prev_grades_json
    prev_grades_json = []
    
    thread = threading.Thread(
        target=run_grabber, 
        args=(
            os.getenv('HTWD_USERNAME'), 
            os.getenv('HTWD_PASSWORD'))
        )
    thread.start()
    
    print(">>> grade_grabber gestartet!")
    
    timestamp = datetime.datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
    send_pushbullet_notification("HTWD Noten Checker", "Der Noten-Checker wurde gestartet ("+timestamp+")!", timestamp)
    