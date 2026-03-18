# TaskTracker

TaskTracker ist eine webbasierte Projekt- und Aufgabenverwaltung, die im Rahmen der DBWE-Praxisarbeit entwickelt wurde.
Benutzer können sich registrieren, anmelden und eigene Projekte mit dazugehörigen Tasks verwalten.

Die Applikation bietet zusätzlich ein RESTful API mit tokenbasierter Authentifizierung, sodass Projektdaten auch ohne Browser mit Clients wie `curl` abgefragt und erstellt werden können.

---

## Funktionen

### Weboberfläche

* Benutzerregistrierung
* Login / Logout
* Dashboard mit Übersicht aller Projekte
* Neues Projekt erstellen
* Projekt-Detailansicht
* Tasks erstellen
* Tasks als erledigt / offen markieren
* Tasks löschen

### Geschäftslogik

* Fortschrittsberechnung pro Projekt in Prozent
* Erkennung überfälliger Tasks

### REST API

* Tokenbasierte Authentifizierung
* Projekte abrufen
* Projekte erstellen
* Tasks eines Projekts abrufen
* Tasks eines Projekts erstellen

---

## Verwendete Technologien

* Python 3
* Flask
* Flask-SQLAlchemy
* Flask-Migrate
* Flask-Login
* Flask-WTF
* Flask-HTTPAuth
* MySQL
* PyMySQL
* Gunicorn
* Nginx (Deployment auf VM)

---

## Datenmodell

Die Applikation verwendet folgende Hauptmodelle:

* User
* Project
* TaskItem

### Beziehungen

* Ein Benutzer besitzt mehrere Projekte
* Ein Projekt besitzt mehrere Tasks

---

## Lokale Installation

### Repository klonen

git clone <REPO-URL>
cd DBWE-Praxisarbeit

### Virtuelle Umgebung erstellen

python3 -m venv .venv
source .venv/bin/activate

### Abhängigkeiten installieren

pip install -r requirements.txt

### Umgebungsvariablen setzen (Beispiel)

export FLASK_APP=microblog.py
export SECRET_KEY='your-secret-key'
export DATABASE_URL='mysql+pymysql://USER:PASSWORD@HOST:PORT/defaultdb?charset=utf8mb4&ssl_ca=/ABSOLUTER/PFAD/ZUR/aiven-ca.pem'

### Datenbankmigrationen anwenden

flask db upgrade

### Anwendung starten

flask run

Danach erreichbar unter:
http://127.0.0.1:5000

---

## API verwenden

### Token erzeugen

curl -u USERNAME:PASSWORD -X POST http://127.0.0.1:5000/api/tokens

### Projekte abrufen

curl -H "Authorization: Bearer TOKEN" http://127.0.0.1:5000/api/projects

### Projekt erstellen

curl -X POST http://127.0.0.1:5000/api/projects 
-H "Authorization: Bearer TOKEN" 
-H "Content-Type: application/json" 
-d '{"name":"API Test Projekt"}'

### Tasks eines Projekts abrufen

curl -H "Authorization: Bearer TOKEN" http://127.0.0.1:5000/api/projects/1/tasks

### Task erstellen

curl -X POST http://127.0.0.1:5000/api/projects/1/tasks 
-H "Authorization: Bearer TOKEN" 
-H "Content-Type: application/json" 
-d '{"title":"API Task","description":"Task via API","due_date":"2026-03-20"}'

---

## Deployment

Die Anwendung wurde auf einer Linux-VM bereitgestellt.
Die Auslieferung erfolgt über:

* Nginx als Reverse Proxy
* Flask-Anwendung auf 127.0.0.1:5000
* MySQL-Datenbank auf Aiven

Öffentliche URL:
http://lab12.ifalabs.org

---

## Projektstruktur

DBWE-Praxisarbeit/
├── app/
│   ├── api/
│   ├── auth/
│   ├── errors/
│   ├── main/
│   ├── templates/
│   ├── **init**.py
│   └── models.py
├── certs/
├── migrations/
├── config.py
├── microblog.py
├── requirements.txt
└── README.md

---

## Hinweis

Dieses Projekt wurde im Rahmen einer Praxisarbeit umgesetzt und fokussiert bewusst auf die geforderten Mindestanforderungen.
