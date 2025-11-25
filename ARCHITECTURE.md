# Architektur

## Komponenten

### 1. Backend Service (`backend.py`)
- **Dummy Website Backend** - Mock-Authentifizierung und Datenabruf
- Die echte Implementierung wird `requests` für Web-Scraping verwenden

### 2. GUI Layer (`login_dialog.py`, `main_window.py`)
- **Main Window** - tkinter-basierte Oberfläche
- **Login Dialog** - Eingabe der Zugangsdaten
- **Data Table** - Anzeige der gesammelten Daten mit Auswahl
- **Action Buttons** - Aktionen auf ausgewählte/alle Zeilen anwenden

### 3. Core Logic (`session_manager.py`, `data_collector.py`, `action_processor.py`)
- **Session Manager** - Verwaltung des Authentifizierungsstatus
- **Data Collector** - Daten von der Website abrufen und parsen
- **Action Processor** - Aktionen auf Dateneinträge ausführen

## Datenfluss

```
Benutzer → Login Dialog → Session Manager → Backend (Auth)
                              ↓
Session Manager → Data Collector → Backend (Daten abrufen)
                              ↓
                        Data Table (Anzeige)
                              ↓
Benutzerauswahl → Action Processor → Backend (Aktion ausführen)
```

## Tech Stack
- **GUI**: tkinter (stdlib, plattformübergreifend)
- **HTTP**: requests
- **Daten**: Python dicts/dataclasses
