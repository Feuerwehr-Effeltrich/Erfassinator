# Bedienungsanleitung

## Anwendung starten

```bash
uv run main.py
```

## Anmeldedaten (Dummy-Backend)

- Benutzername: `admin` / Passwort: `admin`
- Benutzername: `user` / Passwort: `password`

## Funktionen

1. **Anmeldedialog** - Zugangsdaten eingeben zur Authentifizierung
2. **Datentabelle** - Alle abgerufenen Einträge anzeigen mit:
   - ID
   - Titel
   - Datum
   - Status
   - Beschreibung
3. **Daten aktualisieren** - Daten vom Backend neu laden
4. **Berichte erfassen (Auswahl)** - Ausgewählte Zeilen verarbeiten
5. **Berichte erfassen (Alle)** - Alle Einträge auf einmal verarbeiten
6. **Abmelden** - Sitzung beenden und zur Anmeldung zurückkehren

## Nächste Schritte

Um die Integration mit der echten Website durchzuführen:
1. Ersetzen Sie `DummyBackend` in `backend.py` mit der tatsächlichen Implementierung
2. Verwenden Sie `requests` + `BeautifulSoup` für Web-Scraping
3. Aktualisieren Sie das `DataEntry`-Modell in `backend.py` für die echten Daten
4. Implementieren Sie die tatsächliche Aktionslogik in `apply_action()`
