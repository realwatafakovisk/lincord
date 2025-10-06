# Zu LINCORD beitragen

Vielen Dank für Ihr Interesse, zu LINCORD beizutragen! Wir begrüßen Beiträge aus der Community und freuen uns, Sie bei uns zu haben.

## Inhaltsverzeichnis

- [Verhaltenskodex](#verhaltenskodex)
- [Erste Schritte](#erste-schritte)
- [Wie Sie beitragen können](#wie-sie-beitragen-können)
- [Entwicklungsumgebung](#entwicklungsumgebung)
- [Codierungsstandards](#codierungsstandards)
- [Änderungen einreichen](#änderungen-einreichen)
- [Fehler melden](#fehler-melden)
- [Features anfragen](#features-anfragen)
- [Paket-Entwicklung](#paket-entwicklung)

## Verhaltenskodex

Durch die Teilnahme an diesem Projekt verpflichten Sie sich, unseren Verhaltenskodex einzuhalten:

- Seien Sie respektvoll und inklusiv
- Konzentrieren Sie sich auf konstruktives Feedback
- Helfen Sie anderen beim Lernen und Wachsen
- Halten Sie Diskussionen relevant und professionell

## Erste Schritte

1. **Forken Sie das Repository** auf GitHub
2. **Klonen Sie Ihren Fork** lokal:
   ```bash
   git clone https://github.com/ihr-benutzername/lincord.git
   cd lincord
   ```
3. **Richten Sie die Entwicklungsumgebung ein** (siehe [Entwicklungsumgebung](#entwicklungsumgebung))
4. **Erstellen Sie einen neuen Branch** für Ihr Feature:
   ```bash
   git checkout -b feature/ihr-feature-name
   ```

## Wie Sie beitragen können

### Arten von Beiträgen

Wir begrüßen verschiedene Arten von Beiträgen:

- **Fehlerbehebungen** - Beheben Sie Probleme im vorhandenen Code
- **Neue Features** - Fügen Sie neue Terminal-Befehle oder Funktionalitäten hinzu
- **Paket-Entwicklung** - Erstellen Sie neue installierbare Pakete
- **Dokumentation** - Verbessern oder erweitern Sie die Dokumentation
- **Testing** - Fügen Sie Tests hinzu oder verbessern Sie die Testabdeckung
- **Performance** - Optimieren Sie bestehenden Code

### Bereiche, in denen Hilfe benötigt wird

- **Terminal-Befehle** - Fügen Sie weitere Linux-ähnliche Befehle hinzu
- **Moderationstools** - Erweitern Sie Discord-Moderationsfunktionen
- **Datenbankoptimierung** - Verbessern Sie MySQL-Abfragen und -Struktur
- **Fehlerbehandlung** - Bessere Fehlermeldungen und Wiederherstellung
- **Internationalisierung** - Unterstützung für mehrere Sprachen

## Entwicklungsumgebung

### Voraussetzungen

- Python 3.8 oder höher
- MySQL Server (optional, Fallback-Modus verfügbar)
- Discord Bot Token
- Git

### Installation

1. **Abhängigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Umgebungsdatei erstellen**:
   ```bash
   cp .env.example .env
   ```

3. **Umgebung konfigurieren**:
   ```env
   BOT_TOKEN=ihr_test_bot_token
   DB_HOST=localhost
   DB_USER=ihr_db_benutzer
   DB_PASSWORD=ihr_db_passwort
   DB_NAME=lincord_dev
   ```

4. **Bot starten**:
   ```bash
   python main.py
   ```

### Projektstruktur

```
lincord/
├── main.py              # Bot-Initialisierung
├── config.py            # Konfigurationsverwaltung
├── database.py          # Datenbankoperationen
├── cogs/
│   ├── terminal.py      # Kern-Terminal-Interface
│   └── modtools.py      # Moderationstools (kopiert von apt-packages)
├── apt-packages/        # Installierbare Pakete
│   ├── modtools.py      # Echte Discord-Moderation
│   └── ...              # Andere Pakete
└── requirements.txt     # Python-Abhängigkeiten
```

## Codierungsstandards

### Python-Stil

- Befolgen Sie **PEP 8** Stilrichtlinien
- Verwenden Sie **4 Leerzeichen** für Einrückungen
- Maximale Zeilenlänge: **100 Zeichen**
- Verwenden Sie **aussagekräftige Variablennamen**
- Fügen Sie **Docstrings** zu Funktionen und Klassen hinzu

### Beispiel Code-Stil

```python
async def execute_command(self, channel, user, args):
    """Führt einen Terminal-Befehl mit ordnungsgemäßer Fehlerbehandlung aus.
    
    Args:
        channel: Discord-Kanal-Objekt
        user: Discord-Benutzer-Objekt
        args: Liste der Befehlsargumente
        
    Returns:
        bool: True wenn Befehl erfolgreich ausgeführt wurde
    """
    if not args:
        await self.send_error_response(channel, "Kein Befehl angegeben", user)
        return False
        
    command = args[0].lower()
    # Befehlslogik hier verarbeiten
    return True
```

### Commit-Nachrichten

Verwenden Sie klare, beschreibende Commit-Nachrichten:

```
Neuen 'find' Befehl zum Terminal-Interface hinzufügen

- Dateisuch-Funktionalität implementieren
- Unterstützung für Wildcards und Regex hinzufügen
- Ordnungsgemäße Fehlerbehandlung für Berechtigungen einschließen
- Hilfe-Dokumentation aktualisieren

Fixes #123
```

## Änderungen einreichen

### Pull Request Prozess

1. **Stellen Sie sicher, dass Ihr Code** den Codierungsstandards folgt
2. **Testen Sie Ihre Änderungen** gründlich
3. **Aktualisieren Sie die Dokumentation** falls nötig
4. **Erstellen Sie einen Pull Request** mit:
   - Klarem Titel und Beschreibung
   - Verweis auf verwandte Issues
   - Screenshots bei UI-Änderungen
   - Testergebnissen

### Pull Request Vorlage

```markdown
## Beschreibung
Kurze Beschreibung der Änderungen

## Art der Änderung
- [ ] Fehlerbehebung
- [ ] Neues Feature
- [ ] Dokumentations-Update
- [ ] Performance-Verbesserung

## Testing
- [ ] Lokal getestet
- [ ] Tests hinzugefügt/aktualisiert
- [ ] Alle Tests bestehen

## Verwandte Issues
Fixes #(Issue-Nummer)
```

## Fehler melden

### Vor der Meldung

1. **Prüfen Sie bestehende Issues** um Duplikate zu vermeiden
2. **Testen Sie mit der neuesten Version** von LINCORD
3. **Sammeln Sie relevante Informationen**:
   - Python-Version
   - Discord.py-Version
   - Fehlermeldungen/Logs
   - Schritte zur Reproduktion

### Fehlerbericht-Vorlage

```markdown
**Fehlerbeschreibung**
Klare Beschreibung des Fehlers

**Schritte zur Reproduktion**
1. Schritt eins
2. Schritt zwei
3. Schritt drei

**Erwartetes Verhalten**
Was sollte passieren

**Tatsächliches Verhalten**
Was passiert tatsächlich

**Umgebung**
- OS: [z.B., Windows 10]
- Python: [z.B., 3.8.5]
- LINCORD Version: [z.B., 0.0.1]

**Zusätzlicher Kontext**
Alle anderen relevanten Informationen
```

## Features anfragen

### Feature-Anfrage-Richtlinien

1. **Durchsuchen Sie bestehende Anfragen** zuerst
2. **Erklären Sie den Anwendungsfall** klar
3. **Geben Sie Beispiele** wie es funktionieren würde
4. **Berücksichtigen Sie die Implementierungs**-Komplexität

### Feature-Anfrage-Vorlage

```markdown
**Feature-Beschreibung**
Klare Beschreibung des vorgeschlagenen Features

**Anwendungsfall**
Warum wird dieses Feature benötigt?

**Vorgeschlagene Implementierung**
Wie sollte dieses Feature funktionieren?

**Betrachtete Alternativen**
Andere Lösungen, die Sie in Betracht gezogen haben

**Zusätzlicher Kontext**
Alle anderen relevanten Informationen
```

## Paket-Entwicklung

### Neue Pakete erstellen

LINCORD unterstützt installierbare Pakete im `apt-packages/` Verzeichnis:

1. **Paket-Datei erstellen**: `apt-packages/ihr_paket.py`
2. **Cog-Klasse implementieren**:
   ```python
   from discord.ext import commands
   
   class IhrPaket(commands.Cog):
       def __init__(self, bot):
           self.bot = bot
       
       async def execute_ihr_befehl(self, message, args):
           # Befehlsimplementierung
           pass
   
   def setup(bot):
       bot.add_cog(IhrPaket(bot))
   ```

3. **Zum Terminal-Interface hinzufügen** in `cogs/terminal.py`
4. **Installation testen** mit `apt install ihr_paket`

### Paket-Richtlinien

- **Befolgen Sie Namenskonventionen**: Kleinbuchstaben mit Unterstrichen
- **Schließen Sie ordnungsgemäße Fehlerbehandlung ein**
- **Fügen Sie Hilfe-Dokumentation hinzu**
- **Testen Sie gründlich** vor der Einreichung

## Review-Prozess

### Wonach wir suchen

- **Code-Qualität** und Einhaltung von Standards
- **Ordnungsgemäße Tests** und Fehlerbehandlung
- **Klare Dokumentation** und Kommentare
- **Rückwärtskompatibilität** wenn möglich
- **Sicherheitsüberlegungen** für Discord-Bots

### Zeitplan

- **Erste Überprüfung**: Innerhalb von 1 Woche
- **Folge-Überprüfungen**: Innerhalb von 3 Tagen
- **Endgültige Genehmigung**: Wenn alle Anforderungen erfüllt sind

## Hilfe erhalten

### Community-Support

- **GitHub Issues**: Für Fehler und Feature-Anfragen
- **GitHub Discussions**: Für Fragen und allgemeine Diskussionen

### Maintainer-Kontakt

Für sensible Angelegenheiten oder direkte Fragen:
- **E-Mail**: lincord@ixnix.dev
- **GitHub**: @realwatafakovisk

## Anerkennung

Contributors werden anerkannt in:
- **README.md** Contributors-Sektion
- **Release Notes** für bedeutende Beiträge
- **Hall of Fame** für Sicherheitsforscher

Vielen Dank für Ihren Beitrag zu LINCORD! Ihre Bemühungen helfen dabei, dieses Projekt für alle besser zu machen.
