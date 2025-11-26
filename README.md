# Erfassinator

Gesammeltes Erfassen aller Einsatzberichte im FW Portal.

## Starten (Entwicklung)

```bash
uv run erfassinator
```

## Build für Release

```bash
python3 build_pyz.py
```

Erstellt `erfassinator.pyz` und `erfassinator.pyzw` im `dist/` Ordner.

Benutzer brauchen nur Python 3.12+ installiert:
- **Windows:** `pythonw erfassinator.pyzw`
- **Linux/macOS:** `python3 erfassinator.pyz`

## Funktionen

1. **Anmeldung** - Eingabe der Zugangsdaten
2. **Datentabelle** - Zeigt alle abgerufenen Einträge mit:
   - ID (Des Berichtes, nicht des Einsatzes!)
   - Stichwort
   - Datum
   - Status
   - Beschreibung
3. **Daten aktualisieren** - Daten vom Backend neu laden
4. **Berichte erfassen (Auswahl)** - Verarbeite ausgewählte Zeilen
5. **Berichte erfassen (Alle)** - Verarbeite alle Einträge auf einmal (nicht empfohlen)
6. **Abmelden** - Sitzung beenden und zur Anmeldung zurückkehren
