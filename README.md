# LINCORD

<!-- Shields Example, there are N different shields in https://shields.io/ -->
![GitHub last commit](https://img.shields.io/github/last-commit/realwatafakovisk/lincord)
![GitHub language count](https://img.shields.io/github/languages/count/realwatafakovisk/lincord)
![Github repo size](https://img.shields.io/github/repo-size/realwatafakovisk/lincord)
![Github stars](https://img.shields.io/github/stars/realwatafakovisk/lincord?style=social)

> Discord Bot, der eine Linux-ähnliche Terminal-Erfahrung direkt in Discord bietet

## Features

LINCORD bringt die Macht von Linux-Terminal-Befehlen nach Discord:

- **Terminal-Interface**: Führen Sie Linux-ähnliche Befehle direkt in Discord aus
- **Paketverwaltung**: Installieren und verwalten Sie Pakete mit apt-ähnlichen Befehlen
- **Echte Moderation**: Kicken, bannen und timeout-en Sie Benutzer über Terminal-Befehle
- **Dateisystem-Simulation**: Navigieren Sie durch Verzeichnisse mit ls, cd, pwd-Befehlen
- **System-Überwachung**: Überprüfen Sie Prozesse, Speicher und Systeminformationen
- **MySQL-Integration**: Persistente Datenspeicherung und Benutzerverwaltung

## Voraussetzungen

Stellen Sie vor Beginn sicher, dass Sie die folgenden Abhängigkeiten installiert haben:

- **Python 3.8+**: Download von [python.org](https://www.python.org/downloads/)
- **Discord Bot Token**: Erstellen Sie einen Bot im [Discord Developer Portal](https://discord.com/developers/applications)
- **MySQL Server**: Für persistente Datenspeicherung (optional, Fallback-Modus verfügbar)

## Wie Sie das Projekt ausführen

Befolgen Sie die folgenden Schritte, um LINCORD auf Ihrem lokalen Computer auszuführen:

Führen Sie die folgenden Befehle im Projekthauptverzeichnis aus:

### Repository klonen

```bash
git clone https://github.com/realwatafakovisk/lincord
cd lincord
```

Dieser Link ist im grünen Button `Code` zu finden.

### Virtuelle Umgebung erstellen

```bash
python3 -m venv venv
```

**Virtuelle Umgebung aktivieren**

**Unter Windows**

```bash
venv\Scripts\activate
```

**Unter Unix oder MacOS**

```bash
source venv/bin/activate
```

### Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### Bot konfigurieren

1. Erstellen Sie eine `.env` Datei im Projekthauptverzeichnis:

```env
BOT_TOKEN=ihr_discord_bot_token_hier
DB_HOST=ihr_mysql_host
DB_USER=ihr_mysql_benutzer
DB_PASSWORD=ihr_mysql_passwort
DB_NAME=ihr_datenbankname
```

2. Laden Sie den Bot zu Ihrem Discord-Server mit den folgenden Berechtigungen ein:
   - Nachrichten senden
   - Nachrichten verwalten
   - Mitglieder kicken
   - Mitglieder bannen
   - Mitglieder moderieren
   - Kanäle verwalten

### Projekt ausführen

```bash
python main.py
```

Der Bot erstellt automatisch einen Terminal-Kanal, wenn er zum ersten Mal zu einem Server hinzugefügt wird.

## Verfügbare Befehle

Sobald LINCORD auf Ihrem Discord Server läuft, können Sie diese Terminal-Befehle verwenden:

### Grundlegende Befehle
- `ls` - Verzeichnisinhalt auflisten
- `pwd` - Aktuelles Verzeichnis anzeigen
- `cd <verzeichnis>` - Verzeichnis wechseln
- `cat <datei>` - Dateiinhalt anzeigen
- `tree` - Verzeichnisstruktur anzeigen

### System-Befehle
- `ps` - Laufende Prozesse anzeigen
- `top` - Systemressourcen anzeigen
- `free` - Speicherverbrauch anzeigen
- `uptime` - System-Laufzeit-Informationen
- `whoami` - Aktuelle Benutzerinformationen

### Paketverwaltung
- `apt list` - Verfügbare Pakete anzeigen
- `apt install <paket>` - Paket installieren
- `apt remove <paket>` - Paket entfernen
- `apt upgrade` - Alle Pakete aktualisieren

### Moderation (erfordert modtools-Paket)
- `modtools kick <@benutzer> [grund]` - Benutzer kicken
- `modtools ban <@benutzer> [grund]` - Benutzer bannen
- `modtools timeout <@benutzer> <dauer> [grund]` - Benutzer timeout-en
- `modtools clear <anzahl>` - Nachrichten löschen

## Wie Sie beitragen können

Wenn Sie zu diesem Projekt beitragen möchten, befolgen Sie die folgenden Schritte:

1. Forken Sie dieses Repository.
2. Erstellen Sie einen Branch: `git checkout -b <branch_name>`.
3. Nehmen Sie Ihre Änderungen vor und bestätigen Sie sie: `git commit -m '<commit_message>'`
4. Senden Sie an den ursprünglichen Branch: `git push origin <project_name> / <location>`
5. Erstellen Sie den Pull Request.

Alternativ konsultieren Sie die GitHub-Dokumentation zu [wie man einen Pull Request erstellt](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

Weitere Details finden Sie in [CONTRIBUTING.md](CONTRIBUTING.md).

## Lizenz

Dieses Projekt steht unter Lizenz. Siehe [LICENSE](LICENSE) für weitere Informationen.

## Architektur

LINCORD ist mit einer modularen Architektur aufgebaut:

- **main.py** - Bot-Initialisierung und Server-Setup
- **cogs/terminal.py** - Kern-Terminal-Interface und Befehlsverarbeitung
- **apt-packages/** - Installierbare Pakete (modtools, etc.)
- **database.py** - MySQL-Integration und Datenpersistierung
- **config.py** - Konfigurationsverwaltung

## Technischer Stack

- **py-cord 2.4+** - Discord Bot Framework
- **aiomysql** - Async MySQL Connector
- **Python 3.8+** - Kern-Laufzeitumgebung

## Zurück nach oben

[⬆ Zurück nach oben](#lincord)