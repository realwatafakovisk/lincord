import discord
from discord.ext import commands
import asyncio
import os
import json
from pathlib import Path
import config
from database import db_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

activity = discord.CustomActivity("LINCORD v0.0.1")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix=config.BOT_PREFIX, intents=intents, activity=activity)

class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Server aktivieren', style=discord.ButtonStyle.primary, custom_id='setup_server')
    async def setup_server(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        
        if await db_manager.is_server_activated(guild.id):
            embed = discord.Embed(
                title="Fehler",
                description="Dieser Server ist bereits aktiviert!",
                color=config.COLORS['ERROR']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            
            overwrites[interaction.user] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            
            cmd_channel = await guild.create_text_channel(
                config.LINCORD_CMD_CHANNEL,
                overwrites=overwrites,
                topic="LINCORD Terminal Interface - Linux-ähnliche Commands"
            )
            
            await db_manager.activate_server(guild.id, cmd_channel.id)
            
            welcome_embed = discord.Embed(
                title="LINCORD Terminal",
                description=f"Willkommen bei LINCORD, {interaction.user.mention}!\n\n"
                           f"**Aktuelles Verzeichnis:** `/home/{interaction.user.name}`\n\n"
                           f"**Verfügbare Befehle:**\n"
                           f"`ls` - Verzeichnis auflisten\n"
                           f"`pwd` - Aktueller Pfad\n"
                           f"`whoami` - Aktueller Benutzer\n"
                           f"`apt list` - Verfügbare Pakete anzeigen\n"
                           f"`apt install <paket>` - Paket installieren\n"
                           f"`help` - Hilfe anzeigen\n\n"
                           f"Verwende diese Befehle wie in einer echten Linux-Terminal!",
                color=config.COLORS['SUCCESS']
            )
            await cmd_channel.send(embed=welcome_embed)
            
            success_embed = discord.Embed(
                title="Server aktiviert!",
                description=f"LINCORD wurde erfolgreich aktiviert!\n"
                           f"Terminal Channel: {cmd_channel.mention}",
                color=config.COLORS['SUCCESS']
            )
            await interaction.response.send_message(embed=success_embed, ephemeral=True)
            
        except discord.Forbidden:
            error_embed = discord.Embed(
                title="Fehler",
                description="Ich habe nicht die Berechtigung, Channels zu erstellen!",
                color=config.COLORS['ERROR']
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
        except Exception as e:
            error_embed = discord.Embed(
                title="Fehler",
                description=f"Ein unerwarteter Fehler ist aufgetreten: {str(e)}",
                color=config.COLORS['ERROR']
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

@bot.event
async def on_ready():
    print(f'{bot.user} ist online!')
    print(f'Bot ist in {len(bot.guilds)} Servern')
    
    try:
        await db_manager.connect()
        print('MySQL Datenbank verbunden')
    except Exception as e:
        print(f'Fehler bei Datenbankverbindung: {e}')
        print('Bot startet ohne Datenbank (Fallback-Modus)')
    
    try:
        bot.load_extension('cogs.terminal')
        print('Terminal Cog geladen')
    except Exception as e:
        print(f'Fehler beim Laden des Terminal Cogs: {e}')
    
    # Load permission system cogs
    try:
        bot.load_extension('cogs.servergroups')
        print('Server Groups Cog geladen')
    except Exception as e:
        print(f'Fehler beim Laden des Server Groups Cogs: {e}')
    
    try:
        bot.load_extension('cogs.user')
        print('User Management Cog geladen')
    except Exception as e:
        print(f'Fehler beim Laden des User Management Cogs: {e}')
    
    await load_all_available_packages()
    
    bot.add_view(SetupView())

async def load_all_available_packages():
    try:
        packages_dir = Path(config.APT_PACKAGES_DIR)
        if packages_dir.exists():
            for package_file in packages_dir.glob("*.py"):
                if package_file.name != "__init__.py":
                    package_name = package_file.stem
                    
                    cog_file = Path(config.COGS_DIR) / f"{package_name}.py"
                    if not cog_file.exists():
                        import shutil
                        shutil.copy2(package_file, cog_file)
                    
                    if f'cogs.{package_name}' not in bot.extensions:
                        try:
                            bot.load_extension(f'cogs.{package_name}')
                            print(f'Paket {package_name} geladen (verfügbar für Installation)')
                        except Exception as e:
                            print(f'Fehler beim Laden von Paket {package_name}: {e}')
                            
    except Exception as e:
        print(f'Fehler beim Laden verfügbarer Pakete: {e}')

@bot.event
async def on_disconnect():
    await db_manager.close()

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                title="LINCORD Setup",
                description="Danke, dass du LINCORD zu deinem Server hinzugefügt hast!\n\n"
                           "**Was ist LINCORD?**\n"
                           "LINCORD ist ein einzigartiger Discord Bot, der eine Linux-ähnliche Terminal-Erfahrung direkt in Discord bietet. Du kannst Befehle wie in einer echten Linux-Konsole ausführen und sogar eigene 'Pakete' installieren!\n\n"
                           "**So funktioniert's:**\n"
                           "1. Klicke auf den Button unten, um deinen Server zu aktivieren\n"
                           "2. Ein spezieller Terminal-Channel wird erstellt\n"
                           "3. Verwende Linux-ähnliche Befehle in diesem Channel\n"
                           "4. Installiere Pakete mit `apt install <paketname>`\n"
                           "5. Nach der ersten Paket-Installation werden Slash-Commands freigeschaltet!\n\n"
                           "Bereit? Klicke auf den Button!",
                color=config.COLORS['INFO']
            )
            
            view = SetupView()
            await channel.send(embed=embed, view=view)
            break

@bot.command(name='setup')
async def setup_command(ctx):
    embed = discord.Embed(
        title="LINCORD Setup",
        description="Klicke auf den Button unten, um LINCORD auf diesem Server zu aktivieren!",
        color=config.COLORS['INFO']
    )
    
    view = SetupView()
    await ctx.send(embed=embed, view=view)

if __name__ == "__main__":
    if not config.BOT_TOKEN:
        print("BOT_TOKEN nicht gefunden! Bitte füge deinen Bot Token in die .env Datei ein.")
    else:
        try:
            bot.run(config.BOT_TOKEN)
        except discord.LoginFailure:
            print("Ungültiger Bot Token! Bitte überprüfe deinen Token in der .env Datei.")
        except Exception as e:
            print(f"Fehler beim Starten des Bots: {e}")
