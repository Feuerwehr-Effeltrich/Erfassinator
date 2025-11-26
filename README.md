# Erfassinator

Gesammeltes Erfassen aller Einsatzberichte im FW Portal.

Genauer: Status von "Berichte in Erfassung" zu "Berichte erwarten Freigabe" setzen.

## Installation

[uv](https://docs.astral.sh/uv/) muss installiert sein.

## Starten

```bash
uv run main.py
```

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
