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

### Project Structure

```
lincord/
├── main.py              # Bot initialization
├── config.py            # Configuration management
├── database.py          # Database operations
├── cogs/
│   ├── terminal.py      # Core terminal interface
│   └── modtools.py      # Moderation tools (copied from apt-packages)
├── apt-packages/        # Installable packages
│   ├── modtools.py      # Real Discord moderation
│   └── ...              # Other packages
└── requirements.txt     # Python dependencies
```

## Coding Standards

### Python Style

- Follow **PEP 8** style guidelines
- Use **4 spaces** for indentation
- Maximum line length: **100 characters**
- Use **meaningful variable names**
- Add **docstrings** to functions and classes

### Example Code Style

```python
async def execute_command(self, channel, user, args):
    """Execute a terminal command with proper error handling.
    
    Args:
        channel: Discord channel object
        user: Discord user object
        args: List of command arguments
        
    Returns:
        bool: True if command executed successfully
    """
    if not args:
        await self.send_error_response(channel, "No command provided", user)
        return False
        
    command = args[0].lower()
    # Process command logic here
    return True
```

### Commit Messages

Use clear, descriptive commit messages:

```
Add new 'find' command to terminal interface

- Implement file search functionality
- Add support for wildcards and regex
- Include proper error handling for permissions
- Update help documentation

Fixes #123
```

## Submitting Changes

### Pull Request Process

1. **Ensure your code follows** the coding standards
2. **Test your changes** thoroughly
3. **Update documentation** if needed
4. **Create a pull request** with:
   - Clear title and description
   - Reference to related issues
   - Screenshots if UI changes
   - Test results

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tested locally
- [ ] Added/updated tests
- [ ] All tests pass

## Related Issues
Fixes #(issue number)
```

## Reporting Bugs

### Before Reporting

1. **Check existing issues** to avoid duplicates
2. **Test with latest version** of LINCORD
3. **Gather relevant information**:
   - Python version
   - Discord.py version
   - Error messages/logs
   - Steps to reproduce

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 10]
- Python: [e.g., 3.8.5]
- LINCORD Version: [e.g., 2.0.1]

**Additional Context**
Any other relevant information
```

## Requesting Features

### Feature Request Guidelines

1. **Search existing requests** first
2. **Explain the use case** clearly
3. **Provide examples** of how it would work
4. **Consider implementation** complexity

### Feature Request Template

```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why is this feature needed?

**Proposed Implementation**
How should this feature work?

**Alternatives Considered**
Other solutions you've considered

**Additional Context**
Any other relevant information
```

## Package Development

### Creating New Packages

LINCORD supports installable packages in the `apt-packages/` directory:

1. **Create package file**: `apt-packages/your_package.py`
2. **Implement Cog class**:
   ```python
   from discord.ext import commands
   
   class YourPackage(commands.Cog):
       def __init__(self, bot):
           self.bot = bot
       
       async def execute_your_command(self, message, args):
           # Command implementation
           pass
   
   def setup(bot):
       bot.add_cog(YourPackage(bot))
   ```

3. **Add to terminal interface** in `cogs/terminal.py`
4. **Test installation** with `apt install your_package`

### Package Guidelines

- **Follow naming conventions**: lowercase with underscores
- **Include proper error handling**
- **Add help documentation**
- **Test thoroughly** before submitting

## Review Process

### What We Look For

- **Code quality** and adherence to standards
- **Proper testing** and error handling
- **Clear documentation** and comments
- **Backward compatibility** when possible
- **Security considerations** for Discord bots

### Timeline

- **Initial review**: Within 1 week
- **Follow-up reviews**: Within 3 days
- **Final approval**: When all requirements are met

## Getting Help

### Community Support

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Discord Server**: [Join our community](https://discord.gg/lincord) (if available)

### Maintainer Contact

For sensitive issues or direct questions:
- **Email**: maintainer@lincord.dev (if available)
- **GitHub**: @realwatafakovisk

## Recognition

Contributors will be recognized in:
- **README.md** contributors section
- **Release notes** for significant contributions
- **Hall of Fame** for security researchers

Thank you for contributing to LINCORD! Your efforts help make this project better for everyone.
