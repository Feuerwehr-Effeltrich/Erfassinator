# Erfassinator

Gesammeltes Erfassen aller Einsatzberichte im FW Portal.

## Installation

Stellen Sie sicher, dass [uv](https://docs.astral.sh/uv/) installiert ist.

## Starten

```bash
uv run main.py
```

## Anmeldedaten (Dummy-Backend für MVP)

- Benutzername: `admin` / Passwort: `admin`
- Benutzername: `user` / Passwort: `password`

## Funktionen

1. **Anmeldung** - Eingabe der Zugangsdaten
2. **Datentabelle** - Zeigt alle abgerufenen Einträge mit:
   - ID
   - Titel
   - Datum
   - Status
   - Beschreibung
3. **Daten aktualisieren** - Daten vom Backend neu laden
4. **Berichte erfassen (Auswahl)** - Verarbeite ausgewählte Zeilen
5. **Berichte erfassen (Alle)** - Verarbeite alle Einträge auf einmal
6. **Abmelden** - Sitzung beenden und zur Anmeldung zurückkehren

## Nächste Schritte

Um die Integration mit der echten Website durchzuführen:
1. Ersetzen Sie `DummyBackend` in `backend.py` mit der tatsächlichen Implementierung
2. Verwenden Sie `requests` + `beautifulsoup4` für Web-Scraping
3. Aktualisieren Sie das `DataEntry`-Modell, um die echten Daten abzubilden
4. Implementieren Sie die tatsächliche Aktionslogik in `apply_action()`
