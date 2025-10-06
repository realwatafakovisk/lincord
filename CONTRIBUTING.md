down
**Fehlerbeschreibung**
Klare Beschreibung des Fehlers

**Schritte zur Reproduktion**
1. Schritt eins
2. Schritt zwei
3. Schritt drei

**Erwartetes Verhalten**
Was sollte passieren?

**Tatsächliches Verhalten**
Was passiert tatsächlich?

**Umgebung**
- Betriebssystem: [z. B. Windows 10]
- Python: [z. B. 3.8.5]
- LINCORD-Version: [z. B. 0.0.1]

**Zusätzlicher Kontext**
Weitere relevante Informationen
```

## Funktionsanfragen

### Richtlinien für Funktionsanfragen

1. **Vorhandene Anfragen durchsuchen**
2. **Anwendungsfall** klar erläutern
3. **Beispiele** für die Funktionsweise angeben
4. **Komplexität der Implementierung** berücksichtigen

### Vorlage für Funktionsanfragen

```markdown
**Funktionsbeschreibung**
Klare Beschreibung der vorgeschlagenen Funktion

**Anwendungsfall**
Warum wird diese Funktion benötigt?

**Vorgeschlagene Implementierung**
Wie soll diese Funktion funktionieren?

**In Betracht gezogene Alternativen**
Weitere Lösungen, die Sie in Betracht gezogen haben

**Zusätzlicher Kontext**
Weitere relevante Informationen
```

## Paketentwicklung

### Neue Pakete erstellen

LINCORD unterstützt installierbare Pakete im Verzeichnis `apt-packages/`:

1. **Paketdatei erstellen**: `apt-packages/your_package.py`
2. **Cog-Klasse implementieren**:
```python
from discord.ext import commands

class YourPackage(commands.Cog):
def __init__(self, bot):
self.bot = bot

async def execute_your_command(self, message, args):
# Befehlsimplementierung
pass

def setup(bot):
bot.add_cog(YourPackage(bot))
```

3. **Zur Terminaloberfläche hinzufügen** in `cogs/terminal.py`
4. **Installation testen** mit `apt install your_package`

### Paketrichtlinien

- **Namenskonventionen beachten**: Kleinbuchstaben mit Unterstrichen
- **Fehlerbehandlung einbeziehen**
- **Hilfedokumentation hinzufügen**
- **Gründlich testen** vor dem Absenden

## Überprüfungsprozess

### Worauf wir achten

- **Codequalität** und Einhaltung von Standards
- **Sachgemäße Tests** und Fehlerbehandlung
- **Klare Dokumentation** und Kommentare
- **Abwärtskompatibilität**, wenn möglich
- **Sicherheitsüberlegungen** für Discord-Bots

### Zeitplan

- **Erstprüfung**: Innerhalb einer Woche
- **Folgeprüfungen**: Innerhalb von drei Tagen
- **Endgültige Freigabe**: Wenn alle Anforderungen erfüllt sind

## Hilfe erhalten

### Community-Support

- **GitHub-Probleme**: Für Fehler und Funktionsanfragen
- **GitHub-Diskussionen**: Für Fragen und allgemeine Diskussionen

### Kontakt zum Betreuer

Bei sensiblen Problemen oder direkten Fragen:
- **E-Mail**: lincord@ixnix.dev
- **GitHub**: @realwatafakovisk

## Anerkennung

Mitwirkende werden wie folgt erwähnt:
- **README.md**-Bereich für Mitwirkende
- **Release-Notes** für wichtige Beiträge
- **Hall of Fame** für Sicherheitsforscher

Vielen Dank für Ihren Beitrag zu LINCORD! Ihr Engagement trägt dazu bei, dieses Projekt für alle zu verbessern.
