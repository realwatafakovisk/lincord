# Sicherheitsrichtlinie

## Unterstützte Versionen

Die folgenden Versionen von LINCORD werden derzeit mit Sicherheitsupdates unterstützt:

| Version | Unterstützt        |
| ------- | ------------------ |
| 0.0.1   | :white_check_mark: |


## Sicherheitslücke melden

Wir nehmen Sicherheit ernst. Wenn Sie eine Sicherheitslücke in LINCORD entdecken, melden Sie diese bitte verantwortungsvoll.

### Wie melden

**Erstellen Sie KEINE öffentliche GitHub-Issue für Sicherheitslücken.**

Stattdessen:

1. **E-Mail**: Senden Sie Details an `security@lincord.dev` (falls verfügbar)
2. **Private Nachricht**: Kontaktieren Sie den Maintainer direkt auf Discord
3. **GitHub Security Advisories**: Nutzen Sie GitHubs private Schwachstellen-Berichtsfunktion

### Was einzuschließen ist

Bei der Meldung einer Sicherheitslücke bitte folgendes angeben:

- **Beschreibung** der Sicherheitslücke
- **Schritte zur Reproduktion** des Problems
- **Potentielle Auswirkungen** bewerten
- **Lösungsvorschlag** (falls vorhanden)
- **Ihre Kontaktdaten** für Rückfragen

### Bearbeitungsprozess

- **Bestätigung**: Wir bestätigen den Erhalt innerhalb von 48 Stunden
- **Untersuchung**: Wir untersuchen und bewerten die Sicherheitslücke
- **Zeitplan**: Updates alle 5-7 Tage während des Prozesses
- **Lösung**: Kritische Probleme werden innerhalb von 30 Tagen behoben
- **Veröffentlichung**: Koordinierte öffentliche Bekanntgabe nach dem Fix

### Geltungsbereich

Diese Sicherheitsrichtlinie umfasst:

- **Kern-Bot-Funktionalität** (main.py, terminal.py)
- **Datenbankoperationen** (database.py)
- **Moderationstools** (modtools package)
- **Authentifizierung und Berechtigungen**

### Außerhalb des Geltungsbereichs

Folgende Punkte sind generell ausgeschlossen:

- **Drittanbieter-Abhängigkeiten** (an Upstream melden)
- **Discord-Plattform-Probleme**
- **Server-spezifische Fehlkonfigurationen**
- **Social Engineering Angriffe**

## Sicherheits-Best-Practices

Bei der Verwendung von LINCORD:

1. **Bot-Token sicher aufbewahren** - Niemals teilen oder committen
2. **Richtige Discord-Berechtigungen** - Nur nötige Berechtigungen gewähren
3. **Regelmäßige Updates** - LINCORD auf dem neuesten Stand halten
4. **Logs überwachen** - Auf ungewöhnliche Aktivitäten achten
5. **Daten sichern** - Regelmäßige Datenbank-Backups empfohlen

## Hall of Fame

Wir erkennen Sicherheitsforscher an, die helfen, LINCORD zu verbessern:

<!-- Zukünftige Mitwirkende werden hier aufgelistet -->

*Noch keine Sicherheitsberichte erhalten.*

---


**Hinweis**: Diese Sicherheitsrichtlinie gilt für das LINCORD Discord Bot Projekt. Für Discord-Plattform-Sicherheitsprobleme wenden Sie sich direkt an Discord.
