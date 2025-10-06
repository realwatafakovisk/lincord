# LINCORD

<!-- Shields Example, there are N different shields in https://shields.io/ -->
![GitHub last commit](https://img.shields.io/github/last-commit/realwatafakovisk/lincord)
![GitHub language count](https://img.shields.io/github/languages/count/realwatafakovisk/lincord)
![Github repo size](https://img.shields.io/github/repo-size/realwatafakovisk/lincord)
![Github stars](https://img.shields.io/github/stars/realwatafakovisk/lincord?style=social)

> Discord Bot that provides a Linux-like terminal experience directly in Discord

## Features

LINCORD brings the power of Linux terminal commands to Discord:

- **Terminal Interface**: Execute Linux-like commands directly in Discord
- **Package Management**: Install and manage packages with apt-like commands
- **Real Moderation**: Kick, ban, timeout users through terminal commands
- **File System Simulation**: Navigate directories with ls, cd, pwd commands
- **System Monitoring**: Check processes, memory, and system information
- **MySQL Integration**: Persistent data storage and user management

## Prerequisites

Before you begin, make sure you have the following dependencies installed:

- **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/)
- **Discord Bot Token**: Create a bot at [Discord Developer Portal](https://discord.com/developers/applications)
- **MySQL Server**: For persistent data storage (optional, fallback mode available)

## How to run the project

Follow the steps below to run LINCORD on your local machine:

Execute the following commands from the project root folder:

### Clone this repository

```bash
git clone https://github.com/realwatafakovisk/lincord
cd lincord
```

This link can be found in the green button above `Code`.

### Create a Virtual Environment

```bash
python3 -m venv venv
```

**Activate the virtual environment**

**On Windows**

```bash
venv\Scripts\activate
```

**On Unix or MacOS**

```bash
source venv/bin/activate
```

### Install the dependencies

```bash
pip install -r requirements.txt
```

### Configure the bot

1. Create a `.env` file in the project root:

```env
BOT_TOKEN=your_discord_bot_token_here
DB_HOST=your_mysql_host
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name
```

2. Invite the bot to your Discord server with the following permissions:
   - Send Messages
   - Manage Messages
   - Kick Members
   - Ban Members
   - Moderate Members
   - Manage Channels

### Run the project

```bash
python main.py
```

The bot will automatically create a terminal channel when first added to a server.

## Available Commands

Once LINCORD is running in your Discord server, you can use these terminal commands:

### Basic Commands
- `ls` - List directory contents
- `pwd` - Show current directory
- `cd <directory>` - Change directory
- `cat <file>` - Display file contents
- `tree` - Show directory structure

### System Commands
- `ps` - Show running processes
- `top` - Display system resources
- `free` - Show memory usage
- `uptime` - System uptime information
- `whoami` - Current user information

### Package Management
- `apt list` - Show available packages
- `apt install <package>` - Install a package
- `apt remove <package>` - Remove a package
- `apt upgrade` - Upgrade all packages

### Moderation (requires modtools package)
- `modtools kick <@user> [reason]` - Kick a user
- `modtools ban <@user> [reason]` - Ban a user
- `modtools timeout <@user> <duration> [reason]` - Timeout a user
- `modtools clear <amount>` - Delete messages

## How to Contribute

If you want to contribute to this project, follow the steps below:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and confirm them: `git commit -m '<commit_message>'`
4. Send to the original branch: `git push origin <project_name> / <location>`
5. Create the pull request.

Alternatively, consult the GitHub documentation on [how to create a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## License

This project is under license. See [LICENSE](LICENSE) for more information.

## Architecture

LINCORD is built with a modular architecture:

- **main.py** - Bot initialization and server setup
- **cogs/terminal.py** - Core terminal interface and command processing
- **apt-packages/** - Installable packages (modtools, etc.)
- **database.py** - MySQL integration and data persistence
- **config.py** - Configuration management

## Technical Stack

- **py-cord 2.4+** - Discord bot framework
- **aiomysql** - Async MySQL connector
- **Python 3.8+** - Core runtime

## Back to the top

[Back to the top](#lincord)