# Sicherheitsrichtlinie

## Unterstützte Versionen

Die folgenden LINCORD-Versionen werden derzeit mit Sicherheitsupdates unterstützt:

| Version | Unterstützt |
| ------- | ------------------ |
| 0.0.x | :white_check_mark: |

## Sicherheitslücke melden

Wir nehmen Sicherheit ernst. Wenn Sie eine Sicherheitslücke in LINCORD entdecken, melden Sie diese bitte verantwortungsbewusst.

### So melden Sie Sicherheitslücken

**Erstellen Sie KEIN öffentliches GitHub-Problem für Sicherheitslücken.**

Bitte gehen Sie stattdessen wie folgt vor:

1. **E-Mail**: Senden Sie die Details an „lincord@ixnix.dev“.
2. **Private Nachricht**: Kontaktieren Sie den Betreuer direkt über Discord.
3. **GitHub-Sicherheitshinweise**: Nutzen Sie die private Meldefunktion für Sicherheitslücken von GitHub.

### Was Sie angeben sollten

Bitte geben Sie bei der Meldung einer Sicherheitslücke Folgendes an:

- **Beschreibung** der Sicherheitslücke
- **Schritte zur Reproduktion** des Problems
- **Bewertung der potenziellen Auswirkungen**
- **Ihre Kontaktdaten** für die Nachverfolgung

### Antwortprozess

- **Bestätigung**: Wir bestätigen den Eingang innerhalb von 48 Stunden.
- **Untersuchung**: Wir untersuchen und bewerten die Sicherheitslücke.
- **Zeitplan**: Sie erhalten während des Prozesses alle 5–7 Tage Updates.
- **Lösung**: Wir bemühen uns, kritische Probleme zu beheben. Probleme innerhalb von 30 Tagen
- **Offenlegung**: Wir koordinieren die öffentliche Bekanntgabe nach Veröffentlichung des Fixes.

### Geltungsbereich

Diese Sicherheitsrichtlinie umfasst:

- **Kernfunktionen des Bots** (main.py, terminal.py)
- **Datenbankoperationen** (database.py)
- **Moderationstools** (modtools-Paket)
- **Authentifizierung und Berechtigungen**

### Nicht im Geltungsbereich

Folgende Punkte fallen grundsätzlich nicht in den Geltungsbereich:

- **Abhängigkeiten von Drittanbietern** (an Upstream melden)
- **Probleme mit der Discord-Plattform**
- **Serverspezifische Fehlkonfigurationen**
- **Social-Engineering-Angriffe**

## Best Practices für die Sicherheit

Bei der Verwendung von LINCORD:

1. **Schützen Sie Ihren Bot-Token** – Geben Sie ihn niemals weiter und übertragen Sie ihn nicht.
2. **Verwenden Sie die richtigen Discord-Berechtigungen** – Erteilen Sie nur die erforderlichen Berechtigungen.
3. **Regelmäßige Updates** – Halten Sie LINCORD auf dem neuesten Stand.
4. **Überwachen Sie Protokolle** – Achten Sie auf ungewöhnliche Aktivitäten.
5. **Datensicherung** – Regelmäßige Datenbanksicherungen empfohlen

## Hall of Fame

Wir würdigen Sicherheitsforscher, die zur Verbesserung von LINCORD beitragen:

<!-- Zukünftige Mitwirkende werden hier aufgeführt -->

*Bisher keine Sicherheitsberichte eingegangen.*

---

**Hinweis**: Diese Sicherheitsrichtlinie gilt für das LINCORD-Discord-Bot-Projekt. Bei Sicherheitsproblemen auf der Discord-Plattform wenden Sie sich bitte direkt an Discord.
