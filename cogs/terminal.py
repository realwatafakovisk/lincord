import discord
from discord.ext import commands
import os
import json
import asyncio
from pathlib import Path
import config
from database import db_manager

class TerminalInterface(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    
    async def send_terminal_response(self, channel, command, output, user, success=True):
        current_time = discord.utils.utcnow().strftime("%H:%M:%S")
        
        terminal_output = f"```bash\n[{current_time}] {user.name}@lincord:~$ {command}\n{output}\n```"
        
        await channel.send(terminal_output)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if message.channel.name != config.LINCORD_CMD_CHANNEL:
            return
        
        command = message.content.strip()
        if not command:
            return
        
        user = message.author
        
        try:
            await message.delete()
        except:
            pass
        
        await asyncio.sleep(0.1)
        
        await self.process_command(message.channel, command, user, message)
    
    async def process_command(self, channel, command, user, message):
        parts = command.split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd == "ls":
            await self.cmd_ls(channel, user, args)
        elif cmd == "pwd":
            await self.cmd_pwd(channel, user)
        elif cmd == "cd":
            await self.cmd_cd(channel, user, args)
        elif cmd == "cat":
            await self.cmd_cat(channel, user, args)
        elif cmd == "tree":
            await self.cmd_tree(channel, user)
        elif cmd == "find":
            await self.cmd_find(channel, user, args)
        elif cmd == "du":
            await self.cmd_du(channel, user)
        
        elif cmd == "whoami":
            await self.cmd_whoami(channel, user)
        elif cmd == "uname":
            await self.cmd_uname(channel, user, args)
        elif cmd == "ps":
            await self.cmd_ps(channel, user)
        elif cmd == "top":
            await self.cmd_top(channel, user)
        elif cmd == "free":
            await self.cmd_free(channel, user)
        elif cmd == "uptime":
            await self.cmd_uptime(channel, user)
        elif cmd == "env":
            await self.cmd_env(channel, user)
        
        elif cmd == "echo":
            await self.cmd_echo(channel, user, args)
        elif cmd == "date":
            await self.cmd_date(channel, user)
        elif cmd == "clear":
            await self.cmd_clear(channel, user)
        elif cmd == "history":
            await self.cmd_history(channel, user)
        elif cmd == "alias":
            await self.cmd_alias(channel, user)
        elif cmd == "man":
            await self.cmd_man(channel, user, args)
        elif cmd == "help":
            await self.cmd_help(channel, user)
        
        elif cmd == "apt":
            await self.cmd_apt(channel, user, args)
        
        elif cmd == "modtools":
            await self.cmd_modtools(channel, user, args, message)
        elif cmd == "funcommands":
            await self.cmd_funcommands(channel, user, args)
        
        # Permission system commands
        elif cmd == "groups":
            server_groups_cog = self.bot.get_cog("ServerGroups")
            if server_groups_cog:
                await server_groups_cog.execute_groups(message, parts)
            else:
                await self.send_terminal_response(
                    channel, command, 
                    "groups: module not loaded\nTry restarting the bot", 
                    user, success=False
                )
        elif cmd == "user":
            user_management_cog = self.bot.get_cog("UserManagement")
            if user_management_cog:
                await user_management_cog.execute_user(message, parts)
            else:
                await self.send_terminal_response(
                    channel, command, 
                    "user: module not loaded\nTry restarting the bot", 
                    user, success=False
                )
        elif cmd == "login":
            user_management_cog = self.bot.get_cog("UserManagement")
            if user_management_cog:
                await user_management_cog.execute_login(message, parts)
            else:
                await self.send_terminal_response(
                    channel, command, 
                    "login: module not loaded\nTry restarting the bot", 
                    user, success=False
                )
        elif cmd == "logout":
            user_management_cog = self.bot.get_cog("UserManagement")
            if user_management_cog:
                await user_management_cog.execute_logout(message, parts)
            else:
                await self.send_terminal_response(
                    channel, command, 
                    "logout: module not loaded\nTry restarting the bot", 
                    user, success=False
                )
        
        else:
            await self.send_terminal_response(
                channel, command, 
                f"bash: {cmd}: command not found\nType 'help' for available commands or 'man {cmd}' for manual.", 
                user, success=False
            )
    
    async def cmd_ls(self, channel, user, args):
        if not args or args[0] == "~":
            output = "documents/  downloads/  desktop/  pictures/"
        elif args[0] == "/":
            output = "bin/  boot/  dev/  etc/  home/  lib/  opt/  proc/  root/  sys/  tmp/  usr/  var/"
        elif args[0] == "documents":
            output = "projects/  notes.txt  readme.md"
        elif args[0] == "downloads":
            output = "lincord-bot.zip  setup.exe  music/"
        else:
            output = f"ls: cannot access '{args[0]}': No such file or directory"
            await self.send_terminal_response(channel, f"ls {' '.join(args)}", output, user, success=False)
            return
        
        await self.send_terminal_response(channel, f"ls {' '.join(args)}", output, user)
    
    async def cmd_pwd(self, channel, user):
        output = f"/home/{user.name}"
        await self.send_terminal_response(channel, "pwd", output, user)
    
    async def cmd_cd(self, channel, user, args):
        if not args:
            output = f"Changed to /home/{user.name}"
        elif args[0] == "..":
            output = "Changed to /home"
        elif args[0] == "/":
            output = "Changed to /"
        elif args[0] in ["documents", "downloads", "desktop"]:
            output = f"Changed to /home/{user.name}/{args[0]}"
        else:
            output = f"bash: cd: {args[0]}: No such file or directory"
            await self.send_terminal_response(channel, f"cd {' '.join(args)}", output, user, success=False)
            return
        
        await self.send_terminal_response(channel, f"cd {' '.join(args)}", output, user)
    
    async def cmd_cat(self, channel, user, args):
        if not args:
            output = "cat: missing file operand"
            await self.send_terminal_response(channel, "cat", output, user, success=False)
            return
        
        filename = args[0]
        if filename == "lincord.conf":
            output = """# LINCORD Configuration File
server_name=discord_server
version=2.0
terminal_enabled=true
packages_installed=0
last_update=2024-10-06"""
        elif filename == "welcome.txt":
            output = f"""Welcome to LINCORD Terminal, {user.display_name}!

This is a Linux-like terminal interface for Discord.
Type 'help' to see available commands.
Install packages with 'apt install <package_name>'

Happy hacking!"""
        elif filename == "README.md":
            output = """# LINCORD Terminal

A Linux terminal simulation for Discord servers.

## Features
- Full Linux command simulation
- Package management system
- GitHub integration for custom packages
- Terminal-based moderation and fun commands

## Usage
Type 'help' for available commands."""
        else:
            output = f"cat: {filename}: No such file or directory"
            await self.send_terminal_response(channel, f"cat {filename}", output, user, success=False)
            return
        
        await self.send_terminal_response(channel, f"cat {filename}", output, user)
    
    async def cmd_tree(self, channel, user):
        output = f"""/home/{user.name}
├── documents/
│   ├── projects/
│   ├── notes.txt
│   └── README.md
├── downloads/
│   ├── lincord-bot.zip
│   ├── setup.exe
│   └── music/
├── desktop/
│   ├── shortcuts/
│   └── wallpapers/
├── pictures/
│   └── screenshots/
├── lincord.conf
└── welcome.txt

7 directories, 6 files"""
        
        await self.send_terminal_response(channel, "tree", output, user)
    
    async def cmd_find(self, channel, user, args):
        if not args:
            output = "find: missing argument"
            await self.send_terminal_response(channel, "find", output, user, success=False)
            return
        
        search_term = args[0]
        matches = []
        
        files = ["lincord.conf", "welcome.txt", "README.md", "notes.txt", "setup.exe"]
        dirs = ["documents", "downloads", "desktop", "pictures", "projects", "music"]
        
        for file in files:
            if search_term.lower() in file.lower():
                matches.append(f"./documents/{file}")
        
        for dir in dirs:
            if search_term.lower() in dir.lower():
                matches.append(f"./{dir}/")
        
        if matches:
            output = "\n".join(matches)
        else:
            output = f"find: '{search_term}': No such file or directory"
            await self.send_terminal_response(channel, f"find {search_term}", output, user, success=False)
            return
        
        await self.send_terminal_response(channel, f"find {search_term}", output, user)
    
    async def cmd_du(self, channel, user):
        output = """4.0K    ./documents/projects
2.0K    ./documents
8.0K    ./downloads/music
12K     ./downloads
4.0K    ./desktop/shortcuts
2.0K    ./desktop/wallpapers
8.0K    ./desktop
4.0K    ./pictures/screenshots
6.0K    ./pictures
1.0K    ./lincord.conf
2.0K    ./welcome.txt
35K     total"""
        
        await self.send_terminal_response(channel, "du", output, user)
    
    async def cmd_whoami(self, channel, user):
        output = user.name
        await self.send_terminal_response(channel, "whoami", output, user)
    
    async def cmd_clear(self, channel, user):
        try:
            messages = []
            async for message in channel.history(limit=50):
                messages.append(message)
            
            if messages:
                await channel.delete_messages(messages)
            
            embed = discord.Embed(
                title="🧹 Terminal cleared",
                description=f"Terminal wurde von {user.mention} geleert.",
                color=config.COLORS['INFO']
            )
            await channel.send(embed=embed, delete_after=3)
        except:
            await self.send_terminal_response(channel, "clear", "Permission denied", user, success=False)
    
    async def cmd_help(self, channel, user):
        # Split help into multiple messages to avoid Discord's 2000 character limit
        
        # Part 1: Basic commands
        output1 = """LINCORD Terminal v2.0 - Available Commands (1/3):

FILESYSTEM:
  ls [dir]          - List directory contents
  pwd               - Print working directory  
  cd <dir>          - Change directory (simulated)
  cat <file>        - Display file contents
  tree              - Show directory tree
  find <name>       - Find files/directories
  du                - Disk usage information

SYSTEM:
  whoami            - Print current username
  uname [-a]        - System information
  ps                - Show running processes
  top               - System monitor
  free              - Memory usage
  uptime            - System uptime
  env               - Environment variables

UTILITIES:
  echo <text>       - Print text
  date              - Show current date/time
  clear             - Clear terminal
  history           - Command history
  alias             - Show aliases
  man <cmd>         - Manual pages"""
        
        await self.send_terminal_response(channel, "help", output1, user)
        await asyncio.sleep(0.5)
        
        # Part 2: Package manager and permissions
        output2 = """LINCORD Terminal v2.0 - Available Commands (2/3):

PACKAGE MANAGER:
  apt list          - List available packages
  apt install <pkg> - Install package
  apt search <term> - Search packages
  apt suggest <url> - Suggest GitHub repo for custom packages
  apt remove <pkg>  - Remove package
  apt upgrade       - Upgrade all packages

PERMISSION SYSTEM:
  groups role add <@role> <level>   - Add role with permission level (1-5)
  groups role remove <@role>        - Remove role permissions
  groups role list                  - List all role permissions
  user add <@user>                  - Add user to system
  user remove <@user>               - Remove user from system
  user perms add <@user> <level>    - Set user permission level (1-5)
  user perms remove <@user>         - Remove user permissions
  user list                         - List all system users
  user passwd [username]            - Set/change password
  login <username>                  - Login to system
  logout                            - Logout from system"""
        
        await self.send_terminal_response(channel, "help", output2, user)
        await asyncio.sleep(0.5)
        
        # Part 3: Packages and levels
        output3 = """LINCORD Terminal v2.0 - Available Commands (3/3):

INSTALLED PACKAGES:
  modtools <cmd>    - Moderation tools (if installed)
  funcommands <cmd> - Fun commands (if installed)

PERMISSION LEVELS:
  1 - Supporter     - Basic access
  2 - Moderator     - Moderate permissions
  3 - Admin         - Advanced permissions
  4 - Senior Admin  - High-level permissions
  5 - Super Admin   - Full system access

HELP:
  help              - Show this help
  help <command>    - Get help for specific command

Type any command to get started!"""
        
        await self.send_terminal_response(channel, "help", output3, user)
    
    async def cmd_uname(self, channel, user, args):
        if args and args[0] == "-a":
            output = f"Linux lincord-{user.name} 5.4.0-LINCORD #1 SMP Discord PREEMPT {discord.utils.utcnow().strftime('%a %b %d %H:%M:%S UTC %Y')} x86_64 GNU/Linux"
        else:
            output = "Linux"
        
        await self.send_terminal_response(channel, f"uname {' '.join(args)}", output, user)
    
    async def cmd_ps(self, channel, user):
        output = f"""  PID TTY          TIME CMD
 1234 pts/0    00:00:01 lincord-bot
 1235 pts/0    00:00:00 discord-client
 1236 pts/0    00:00:02 terminal-interface
 1237 pts/0    00:00:00 database-manager
 1238 pts/0    00:00:01 {user.name}-session"""
        
        await self.send_terminal_response(channel, "ps", output, user)
    
    async def cmd_top(self, channel, user):
        import random
        cpu_usage = random.randint(5, 25)
        mem_usage = random.randint(256, 512)
        
        output = f"""top - {discord.utils.utcnow().strftime('%H:%M:%S')} up 2 days, 14:32, 1 user, load average: 0.{random.randint(10,99)}, 0.{random.randint(10,99)}, 0.{random.randint(10,99)}
Tasks: 142 total, 1 running, 141 sleeping, 0 stopped, 0 zombie
%Cpu(s): {cpu_usage}.2 us, 2.1 sy, 0.0 ni, {100-cpu_usage-2}.7 id, 0.0 wa, 0.0 hi, 0.0 si, 0.0 st
MiB Mem: 1024.0 total, {1024-mem_usage}.3 free, {mem_usage}.7 used, 32.0 buff/cache

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
 1234 lincord   20   0  128532  45612  12456 S   2.1   4.5   0:12.34 lincord-bot
 1235 discord   20   0   89234  23145   8934 S   1.2   2.3   0:08.21 discord-client"""
        
        await self.send_terminal_response(channel, "top", output, user)
    
    async def cmd_free(self, channel, user):
        import random
        used = random.randint(256, 512)
        free = 1024 - used
        
        output = f"""              total        used        free      shared  buff/cache   available
Mem:           1024         {used}         {free}          12          32         {free-32}
Swap:          2048           0        2048"""
        
        await self.send_terminal_response(channel, "free", output, user)
    
    async def cmd_uptime(self, channel, user):
        import random
        days = random.randint(1, 30)
        hours = random.randint(1, 23)
        minutes = random.randint(1, 59)
        
        output = f" {discord.utils.utcnow().strftime('%H:%M:%S')} up {days} days, {hours}:{minutes:02d}, 1 user, load average: 0.{random.randint(10,99)}, 0.{random.randint(10,99)}, 0.{random.randint(10,99)}"
        
        await self.send_terminal_response(channel, "uptime", output, user)
    
    async def cmd_env(self, channel, user):
        output = f"""PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOME=/home/{user.name}
USER={user.name}
SHELL=/bin/bash
TERM=xterm-256color
LANG=en_US.UTF-8
DISCORD_SERVER={channel.guild.name}
LINCORD_VERSION=2.0
PWD=/home/{user.name}"""
        
        await self.send_terminal_response(channel, "env", output, user)
    
    async def cmd_date(self, channel, user):
        import datetime
        current_time = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y")
        await self.send_terminal_response(channel, "date", current_time, user)
    
    async def cmd_echo(self, channel, user, args):
        output = " ".join(args) if args else ""
        await self.send_terminal_response(channel, f"echo {' '.join(args)}", output, user)
    
    async def cmd_history(self, channel, user):
        commands = [
            "ls", "pwd", "whoami", "apt list", "apt install modtools", 
            "modtools --help", "ps", "top", "free", "history"
        ]
        
        output = ""
        for i, cmd in enumerate(commands, 1):
            output += f"  {i:3d}  {cmd}\n"
        
        await self.send_terminal_response(channel, "history", output.strip(), user)
    
    async def cmd_alias(self, channel, user):
        output = """alias ll='ls -l'
alias la='ls -la'
alias l='ls'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias mkdir='mkdir -p'
alias h='history'
alias c='clear'"""
        
        await self.send_terminal_response(channel, "alias", output, user)
    
    async def cmd_man(self, channel, user, args):
        if not args:
            output = "What manual page do you want?"
            await self.send_terminal_response(channel, "man", output, user, success=False)
            return
        
        cmd = args[0].lower()
        manpages = {
            "ls": "LS(1) - list directory contents\n\nSYNOPSIS: ls [OPTION]... [FILE]...\n\nDESCRIPTION: List information about the FILEs (the current directory by default).",
            "pwd": "PWD(1) - print name of current/working directory\n\nSYNOPSIS: pwd\n\nDESCRIPTION: Print the full filename of the current working directory.",
            "whoami": "WHOAMI(1) - print effective username\n\nSYNOPSIS: whoami\n\nDESCRIPTION: Print the user name associated with the current effective user ID.",
            "apt": "APT(8) - command-line package manager\n\nSYNOPSIS: apt [options] command\n\nDESCRIPTION: apt provides a high-level commandline interface for the package management system.",
            "echo": "ECHO(1) - display a line of text\n\nSYNOPSIS: echo [SHORT-OPTION]... [STRING]...\n\nDESCRIPTION: Echo the STRINGs to standard output.",
            "help": "HELP - display available commands\n\nSYNOPSIS: help [command]\n\nDESCRIPTION: Display information about builtin commands."
        }
        
        if cmd in manpages:
            output = manpages[cmd]
        else:
            output = f"No manual entry for {cmd}"
            await self.send_terminal_response(channel, f"man {cmd}", output, user, success=False)
            return
        
        await self.send_terminal_response(channel, f"man {cmd}", output, user)
    
    async def cmd_apt(self, channel, user, args):
        if not args:
            output = "Usage: apt [list|install] [package_name]"
            await self.send_terminal_response(channel, "apt", output, user, success=False)
            return
        
        subcommand = args[0].lower()
        
        if subcommand == "list":
            packages_dir = Path(config.APT_PACKAGES_DIR)
            if packages_dir.exists():
                packages = []
                for file in packages_dir.glob("*.py"):
                    if file.name != "__init__.py":
                        package_name = file.stem
                        packages.append(f"  {package_name}")
                
                if packages:
                    output = "Available packages:\n" + "\n".join(packages)
                else:
                    output = "No packages available in apt-packages directory"
            else:
                output = "apt-packages directory not found"
            
            await self.send_terminal_response(channel, "apt list", output, user)
        
        elif subcommand == "install":
            if len(args) < 2:
                output = "Usage: apt install <package_name>"
                await self.send_terminal_response(channel, "apt install", output, user, success=False)
                return
            
            package_name = args[1]
            await self.install_package(channel, user, package_name)
        
        elif subcommand == "search":
            if len(args) < 2:
                output = "Usage: apt search <search_term>"
                await self.send_terminal_response(channel, "apt search", output, user, success=False)
                return
            
            search_term = args[1].lower()
            await self.search_packages(channel, user, search_term)
        
        elif subcommand == "suggest":
            if len(args) < 2:
                output = """Usage: apt suggest <github_url>

Submit a GitHub repository containing custom packages for LINCORD.

Example:
  apt suggest https://github.com/username/lincord-custom-packages

Requirements:
- Repository must contain Python files with Discord Cogs
- Each file should follow LINCORD package structure
- Include a README.md with package descriptions"""
                await self.send_terminal_response(channel, "apt suggest", output, user, success=False)
                return
            
            github_url = args[1]
            await self.suggest_package(channel, user, github_url)
        
        elif subcommand == "remove":
            if len(args) < 2:
                output = "Usage: apt remove <package_name>"
                await self.send_terminal_response(channel, "apt remove", output, user, success=False)
                return
            
            package_name = args[1]
            await self.remove_package(channel, user, package_name)
        
        elif subcommand == "upgrade":
            await self.upgrade_packages(channel, user)
        
        else:
            output = f"""Unknown apt command: {subcommand}

Available commands:
  apt list           - List available packages
  apt search <term>  - Search for packages
  apt install <pkg>  - Install a package
  apt remove <pkg>   - Remove a package
  apt suggest <url>  - Suggest GitHub repo for custom packages
  apt upgrade        - Upgrade all packages"""
            await self.send_terminal_response(channel, f"apt {subcommand}", output, user, success=False)
    
    async def install_package(self, channel, user, package_name):
        package_file = Path(config.APT_PACKAGES_DIR) / f"{package_name}.py"
        
        if not package_file.exists():
            output = f"Package '{package_name}' not found in repository"
            await self.send_terminal_response(channel, f"apt install {package_name}", output, user, success=False)
            return
        
        try:
            if await db_manager.is_package_installed(channel.guild.id, package_name):
                output = f"Package '{package_name}' is already installed"
                await self.send_terminal_response(channel, f"apt install {package_name}", output, user, success=False)
                return
            
            await self.send_terminal_response(
                channel, f"apt install {package_name}",
                f"Reading package lists... Done\nBuilding dependency tree... Done\nThe following NEW packages will be installed:\n  {package_name}\n0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.",
                user
            )

            await asyncio.sleep(1)
            
            success = await db_manager.install_package(channel.guild.id, package_name)
            if not success:
                output = f"Failed to install package '{package_name}'"
                await self.send_terminal_response(channel, f"apt install {package_name}", output, user, success=False)
                return
            
            await self.send_terminal_response(
                channel, f"apt install {package_name}",
                f"Package '{package_name}' installed successfully\nVersion: 1.2.0\nDescription: {package_name} commands now available\nSize: 1024 bytes\n\nUse '{package_name} --help' to see available commands",
                user
            )
                
        except Exception as e:
            output = f"Failed to install package '{package_name}': {str(e)}"
            await self.send_terminal_response(channel, f"apt install {package_name}", output, user, success=False)
    
    async def search_packages(self, channel, user, search_term):
        packages_dir = Path(config.APT_PACKAGES_DIR)
        matches = []
        
        if packages_dir.exists():
            for file in packages_dir.glob("*.py"):
                if file.name != "__init__.py":
                    package_name = file.stem
                    if search_term in package_name.lower():
                        descriptions = {
                            "modtools": "Moderation tools for server management",
                            "funcommands": "Entertainment commands and games",
                            "utils": "Utility commands for everyday use",
                            "music": "Music bot functionality",
                            "games": "Interactive games and activities"
                        }
                        desc = descriptions.get(package_name, "Custom package functionality")
                        matches.append(f"{package_name} - {desc}")
        
        if matches:
            output = f"Packages matching '{search_term}':\n" + "\n".join([f"  {match}" for match in matches])
        else:
            output = f"No packages found matching '{search_term}'"
        
        await self.send_terminal_response(channel, f"apt search {search_term}", output, user)
    
    async def suggest_package(self, channel, user, github_url):
        if not github_url.startswith("https://github.com/"):
            output = "Invalid GitHub URL. Must start with 'https://github.com/'"
            await self.send_terminal_response(channel, f"apt suggest {github_url}", output, user, success=False)
            return
        
        await self.send_terminal_response(
            channel, f"apt suggest {github_url}",
            f"Analyzing repository: {github_url}",
            user
        )
        
        await asyncio.sleep(2) 
        
        output = f"""Package suggestion submitted successfully!

Repository: {github_url}
Submitted by: {user.display_name}
Status: Under review

Your custom packages will be reviewed by the LINCORD team.
If approved, they will be added to the official repository.

Track your submission: https://github.com/lincord-project/packages/issues

Thank you for contributing to the LINCORD ecosystem!"""
        
        await self.send_terminal_response(channel, f"apt suggest {github_url}", output, user)
    
    async def remove_package(self, channel, user, package_name):
        if not await db_manager.is_package_installed(channel.guild.id, package_name):
            output = f"Package '{package_name}' is not installed"
            await self.send_terminal_response(channel, f"apt remove {package_name}", output, user, success=False)
            return
        
        try:
            success = await db_manager.remove_package(channel.guild.id, package_name)
            if success:
                output = f"Package '{package_name}' removed successfully"
            else:
                output = f"Failed to remove package '{package_name}'"
                await self.send_terminal_response(channel, f"apt remove {package_name}", output, user, success=False)
                return
        except Exception as e:
            output = f"Failed to remove package '{package_name}': {str(e)}"
            await self.send_terminal_response(channel, f"apt remove {package_name}", output, user, success=False)
            return
        
        await self.send_terminal_response(channel, f"apt remove {package_name}", output, user)
    
    async def upgrade_packages(self, channel, user):
        try:
            installed_packages = await db_manager.get_installed_packages(channel.guild.id)
            
            if not installed_packages:
                output = "No packages installed to upgrade"
                await self.send_terminal_response(channel, "apt upgrade", output, user)
                return
            
            await self.send_terminal_response(
                channel, "apt upgrade",
                f"Reading package lists... Done\nBuilding dependency tree... Done\nCalculating upgrade... Done\nThe following packages will be upgraded:\n  " + " ".join(installed_packages),
                user
            )
            
            await asyncio.sleep(2)
            
            output = f"Successfully upgraded {len(installed_packages)} packages:\n"
            for pkg in installed_packages:
                output += f"  {pkg} (1.2.0 -> 1.3.0)\n"
            
            output += f"\n{len(installed_packages)} upgraded, 0 newly installed, 0 to remove."
            
        except Exception as e:
            output = f"Failed to upgrade packages: {str(e)}"
            await self.send_terminal_response(channel, "apt upgrade", output, user, success=False)
            return
        
        await self.send_terminal_response(channel, "apt upgrade", output.strip(), user)
    
    async def cmd_modtools(self, channel, user, args, message):
        if not await db_manager.is_package_installed(channel.guild.id, "modtools"):
            await self.send_terminal_response(
                channel, f"modtools {' '.join(args)}", 
                "bash: modtools: command not found\nInstall with: apt install modtools", 
                user, success=False
            )
            return
        
        modtools_cog = self.bot.get_cog("ModTools")
        if not modtools_cog:
            await self.send_terminal_response(
                channel, f"modtools {' '.join(args)}", 
                "ModTools cog not loaded", 
                user, success=False
            )
            return
        
        if not args:
            output = """ModTools v2.0 - REAL Discord Moderation

Usage: modtools <command> [options]

COMMANDS:
  kick <@user|id> [reason]        - Kick a user from server
  ban <@user|id> [reason]         - Ban a user from server
  timeout <@user|id> <time> [reason] - Timeout a user
  clear <amount>                  - Delete messages (1-100)

EXAMPLES:
  modtools kick @user spamming
  modtools ban 123456789 harassment
  modtools timeout @user 5m being disruptive
  modtools clear 10

WARNING: These are REAL moderation actions!"""
            await self.send_terminal_response(channel, "modtools", output, user)
            return
        
        subcmd = args[0].lower()
        
        if subcmd == "kick":
            await modtools_cog.execute_kick(message, args)
        elif subcmd == "ban":
            await modtools_cog.execute_ban(message, args)
        elif subcmd == "timeout":
            await modtools_cog.execute_timeout(message, args)
        elif subcmd == "clear":
            await modtools_cog.execute_clear(message, args)
        else:
            await self.send_terminal_response(
                channel, f"modtools {' '.join(args)}", 
                f"Unknown command: {subcmd}\nUse 'modtools' without arguments for help", 
                user, success=False
            )
    
    async def cmd_funcommands(self, channel, user, args):
        if not await db_manager.is_package_installed(channel.guild.id, "funcommands"):
            await self.send_terminal_response(
                channel, f"funcommands {' '.join(args)}", 
                "bash: funcommands: command not found\nInstall with: apt install funcommands", 
                user, success=False
            )
            return
        
        if not args:
            output = "FunCommands v1.0.0 - Entertainment Commands\n\nUsage: funcommands <command>\n\nCommands:\n  joke                      - Get a random joke\n  fact                      - Get a random fact\n  8ball <question>          - Ask the magic 8-ball"
            await self.send_terminal_response(channel, "funcommands", output, user)
            return
        
        subcmd = args[0].lower()
        
        if subcmd == "joke":
            import random
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
                "Why don't eggs tell jokes? They'd crack each other up!",
                "What do you call a fake noodle? An impasta!"
            ]
            output = f"🤣 Random Joke:\n{random.choice(jokes)}"
            await self.send_terminal_response(channel, "funcommands joke", output, user)
        
        elif subcmd == "fact":
            import random
            facts = [
                "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
                "A group of flamingos is called a 'flamboyance'.",
                "Octopuses have three hearts and blue blood.",
                "The shortest war in history lasted only 38 to 45 minutes."
            ]
            output = f"🧠 Random Fact:\n{random.choice(facts)}"
            await self.send_terminal_response(channel, "funcommands fact", output, user)
        
        elif subcmd == "8ball" and len(args) >= 2:
            import random
            answers = [
                "It is certain", "Reply hazy, try again", "Don't count on it",
                "It is decidedly so", "Ask again later", "My reply is no",
                "Without a doubt", "Better not tell you now", "My sources say no",
                "Yes definitely", "Cannot predict now", "Outlook not so good"
            ]
            question = " ".join(args[1:])
            output = f"🎱 Magic 8-Ball\nQuestion: {question}\nAnswer: {random.choice(answers)}"
            await self.send_terminal_response(channel, f"funcommands 8ball {question}", output, user)
        
        else:
            output = f"funcommands: invalid command '{subcmd}'\nUse 'funcommands' without arguments for help"
            await self.send_terminal_response(channel, f"funcommands {' '.join(args)}", output, user, success=False)

def setup(bot):
    bot.add_cog(TerminalInterface(bot))
