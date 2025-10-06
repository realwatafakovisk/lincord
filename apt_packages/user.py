import discord
from discord.ext import commands
import asyncio
import hashlib
import secrets
from database import db_manager

class UserManagement(commands.Cog):
    """User management and authentication system"""
    
    def __init__(self, bot):
        self.bot = bot
        self.logged_in_users = {}  # {user_id: {'logged_in': True, 'session': 'token'}}
        self.login_attempts = {}   # Rate limiting
    
    async def send_user_response(self, channel, command, result, user, success=True):
        """Send user response in terminal style"""
        current_time = discord.utils.utcnow().strftime("%H:%M:%S")
        
        # Check if user is logged in
        login_status = self.get_login_display(user)
        
        terminal_output = f"```bash\n[{current_time}] {login_status}@user:~$ {command}\n{result}\n```"
        await channel.send(terminal_output)
    
    def get_login_display(self, user):
        """Get login display name"""
        if user.id in self.logged_in_users and self.logged_in_users[user.id].get('logged_in'):
            username = self.logged_in_users[user.id].get('username', user.name)
            return username
        else:
            return "guest"
    
    async def execute_user(self, message, args):
        """Execute user commands"""
        if len(args) < 2:
            await self.send_user_response(
                message.channel,
                " ".join(args),
                "Usage: user <command> [options]\n\nCommands:\n  add <@user>              - Add user to system\n  remove <@user>           - Remove user from system\n  perms add <@user> <level> - Set user permission level (1-5)\n  perms remove <@user>     - Remove user permissions\n  list                     - List all users\n  passwd [username]        - Set/change password",
                message.author,
                False
            )
            return
        
        subcmd = args[1].lower()
        
        if subcmd == "add":
            await self.add_user(message, args[2:])
        elif subcmd == "remove":
            await self.remove_user(message, args[2:])
        elif subcmd == "perms":
            await self.handle_perms_command(message, args[2:])
        elif subcmd == "list":
            await self.list_users(message)
        elif subcmd == "passwd":
            await self.set_password(message, args[2:])
        else:
            await self.send_user_response(
                message.channel,
                " ".join(args),
                f"Unknown command: {subcmd}\nUse 'user' without arguments for help",
                message.author,
                False
            )
    
    async def execute_login(self, message, args):
        """Handle login command"""
        if len(args) < 2:
            await self.send_user_response(
                message.channel,
                "login",
                "Usage: login <username>",
                message.author,
                False
            )
            return
        
        username = args[1]
        
        # Check if user exists
        user_data = await db_manager.get_user_by_username(message.guild.id, username)
        if not user_data:
            await self.send_user_response(
                message.channel,
                f"login {username}",
                f"User '{username}' not found",
                message.author,
                False
            )
            return
        
        # Check if already logged in
        if message.author.id in self.logged_in_users and self.logged_in_users[message.author.id].get('logged_in'):
            current_user = self.logged_in_users[message.author.id].get('username', 'unknown')
            await self.send_user_response(
                message.channel,
                f"login {username}",
                f"Already logged in as '{current_user}'\nUse 'logout' first",
                message.author,
                False
            )
            return
        
        # Prompt for password
        await self.send_user_response(
            message.channel,
            f"login {username}",
            f"Password for {username}:",
            message.author,
            True
        )
        
        # Wait for password input
        def check(m):
            return m.author == message.author and m.channel == message.channel
        
        try:
            password_msg = await self.bot.wait_for('message', check=check, timeout=30.0)
            await password_msg.delete()  # Delete password message immediately
            
            # Verify password
            if await self.verify_password(message.guild.id, username, password_msg.content):
                # Login successful
                session_token = secrets.token_hex(16)
                self.logged_in_users[message.author.id] = {
                    'logged_in': True,
                    'username': username,
                    'session': session_token,
                    'discord_id': message.author.id
                }
                
                user_level = await db_manager.get_user_permission_level(message.guild.id, message.author.id)
                level_name = self.get_level_name(user_level)
                
                result = f"""LOGIN SUCCESSFUL
User: {username}
Permission Level: {user_level} ({level_name})
Session: Active
Status: Authenticated"""
                
                await self.send_user_response(
                    message.channel,
                    f"login {username}",
                    result,
                    message.author,
                    True
                )
            else:
                await self.send_user_response(
                    message.channel,
                    f"login {username}",
                    "Authentication failed: Invalid password",
                    message.author,
                    False
                )
        
        except asyncio.TimeoutError:
            await self.send_user_response(
                message.channel,
                f"login {username}",
                "Login timeout: No password provided",
                message.author,
                False
            )
    
    async def execute_logout(self, message, args):
        """Handle logout command"""
        if message.author.id not in self.logged_in_users or not self.logged_in_users[message.author.id].get('logged_in'):
            await self.send_user_response(
                message.channel,
                "logout",
                "Not logged in",
                message.author,
                False
            )
            return
        
        username = self.logged_in_users[message.author.id].get('username', 'unknown')
        del self.logged_in_users[message.author.id]
        
        await self.send_user_response(
            message.channel,
            "logout",
            f"Logged out from '{username}'",
            message.author,
            True
        )
    
    async def add_user(self, message, args):
        """Add user to system"""
        if not args:
            await self.send_user_response(
                message.channel,
                "user add",
                "Usage: user add <@user>",
                message.author,
                False
            )
            return
        
        # Check permissions
        if not await self.check_permission(message.author, message.guild, 3):
            await self.send_user_response(
                message.channel,
                " ".join(["user", "add"] + args),
                "Permission denied: You need Admin (level 3) permissions",
                message.author,
                False
            )
            return
        
        user_mention = args[0]
        
        # Extract user ID
        if user_mention.startswith('<@') and user_mention.endswith('>'):
            user_id = int(user_mention[3:-1] if not user_mention.startswith('<@!') else user_mention[3:-1])
        else:
            await self.send_user_response(
                message.channel,
                " ".join(["user", "add"] + args),
                "Invalid user format. Use @user mention",
                message.author,
                False
            )
            return
        
        # Get user object
        target_user = message.guild.get_member(user_id)
        if not target_user:
            await self.send_user_response(
                message.channel,
                " ".join(["user", "add"] + args),
                f"User not found: {user_mention}",
                message.author,
                False
            )
            return
        
        try:
            # Generate default username and password
            username = target_user.name.lower()
            default_password = secrets.token_urlsafe(8)
            
            await db_manager.add_system_user(message.guild.id, user_id, username, default_password)
            
            result = f"""USER ADDED TO SYSTEM
User: {target_user.display_name} ({user_id})
Username: {username}
Default Password: {default_password}
Permission Level: 0 (Guest)
Added by: {message.author.display_name}

IMPORTANT: User should change password with 'user passwd {username}'"""
            
            await self.send_user_response(
                message.channel,
                " ".join(["user", "add"] + args),
                result,
                message.author,
                True
            )
        except Exception as e:
            await self.send_user_response(
                message.channel,
                " ".join(["user", "add"] + args),
                f"Error adding user: {str(e)}",
                message.author,
                False
            )
    
    async def remove_user(self, message, args):
        """Remove user from system"""
        if not args:
            await self.send_user_response(
                message.channel,
                "user remove",
                "Usage: user remove <@user>",
                message.author,
                False
            )
            return
        
        # Check permissions
        if not await self.check_permission(message.author, message.guild, 3):
            await self.send_user_response(
                message.channel,
                " ".join(["user", "remove"] + args),
                "Permission denied: You need Admin (level 3) permissions",
                message.author,
                False
            )
            return
        
        user_mention = args[0]
        
        # Extract user ID
        if user_mention.startswith('<@') and user_mention.endswith('>'):
            user_id = int(user_mention[3:-1] if not user_mention.startswith('<@!') else user_mention[3:-1])
        else:
            await self.send_user_response(
                message.channel,
                " ".join(["user", "remove"] + args),
                "Invalid user format. Use @user mention",
                message.author,
                False
            )
            return
        
        try:
            await db_manager.remove_system_user(message.guild.id, user_id)
            
            # Logout user if currently logged in
            if user_id in self.logged_in_users:
                del self.logged_in_users[user_id]
            
            target_user = message.guild.get_member(user_id)
            user_name = target_user.display_name if target_user else f"User {user_id}"
            
            result = f"""USER REMOVED FROM SYSTEM
User: {user_name} ({user_id})
Removed by: {message.author.display_name}
Status: User access revoked"""
            
            await self.send_user_response(
                message.channel,
                " ".join(["user", "remove"] + args),
                result,
                message.author,
                True
            )
        except Exception as e:
            await self.send_user_response(
                message.channel,
                " ".join(["user", "remove"] + args),
                f"Error removing user: {str(e)}",
                message.author,
                False
            )
    
    async def handle_perms_command(self, message, args):
        """Handle permission commands"""
        if not args:
            await self.send_user_response(
                message.channel,
                "user perms",
                "Usage: user perms <add|remove> <@user> [level]",
                message.author,
                False
            )
            return
        
        action = args[0].lower()
        
        if action == "add":
            await self.add_user_perms(message, args[1:])
        elif action == "remove":
            await self.remove_user_perms(message, args[1:])
        else:
            await self.send_user_response(
                message.channel,
                f"user perms {action}",
                f"Unknown action: {action}\nUse: add or remove",
                message.author,
                False
            )
    
    async def add_user_perms(self, message, args):
        """Add user permissions"""
        if len(args) < 2:
            await self.send_user_response(
                message.channel,
                "user perms add",
                "Usage: user perms add <@user> <level>\nLevel: 1-5 (1=Supporter, 5=Super Admin)",
                message.author,
                False
            )
            return
        
        # Check permissions (only Super Admin can manage user permissions)
        if not await self.check_permission(message.author, message.guild, 5):
            await self.send_user_response(
                message.channel,
                " ".join(["user", "perms", "add"] + args),
                "Permission denied: You need Super Admin (level 5) permissions",
                message.author,
                False
            )
            return
        
        user_mention = args[0]
        try:
            level = int(args[1])
            if level < 1 or level > 5:
                raise ValueError("Invalid level")
        except ValueError:
            await self.send_user_response(
                message.channel,
                " ".join(["user", "perms", "add"] + args),
                "Invalid permission level. Use 1-5",
                message.author,
                False
            )
            return
        
        # Extract user ID
        if user_mention.startswith('<@') and user_mention.endswith('>'):
            user_id = int(user_mention[3:-1] if not user_mention.startswith('<@!') else user_mention[3:-1])
        else:
            await self.send_user_response(
                message.channel,
                " ".join(["user", "perms", "add"] + args),
                "Invalid user format. Use @user mention",
                message.author,
                False
            )
            return
        
        try:
            await db_manager.set_user_permission_level(message.guild.id, user_id, level)
            
            target_user = message.guild.get_member(user_id)
            user_name = target_user.display_name if target_user else f"User {user_id}"
            level_name = self.get_level_name(level)
            
            result = f"""USER PERMISSIONS SET
User: {user_name} ({user_id})
Permission Level: {level} ({level_name})
Set by: {message.author.display_name}
Status: Permissions updated"""
            
            await self.send_user_response(
                message.channel,
                " ".join(["user", "perms", "add"] + args),
                result,
                message.author,
                True
            )
        except Exception as e:
            await self.send_user_response(
                message.channel,
                " ".join(["user", "perms", "add"] + args),
                f"Error setting permissions: {str(e)}",
                message.author,
                False
            )
    
    async def remove_user_perms(self, message, args):
        """Remove user permissions"""
        if not args:
            await self.send_user_response(
                message.channel,
                "user perms remove",
                "Usage: user perms remove <@user>",
                message.author,
                False
            )
            return
        
        # Check permissions
        if not await self.check_permission(message.author, message.guild, 5):
            await self.send_user_response(
                message.channel,
                " ".join(["user", "perms", "remove"] + args),
                "Permission denied: You need Super Admin (level 5) permissions",
                message.author,
                False
            )
            return
        
        user_mention = args[0]
        
        # Extract user ID
        if user_mention.startswith('<@') and user_mention.endswith('>'):
            user_id = int(user_mention[3:-1] if not user_mention.startswith('<@!') else user_mention[3:-1])
        else:
            await self.send_user_response(
                message.channel,
                " ".join(["user", "perms", "remove"] + args),
                "Invalid user format. Use @user mention",
                message.author,
                False
            )
            return
        
        try:
            await db_manager.remove_user_permission_level(message.guild.id, user_id)
            
            target_user = message.guild.get_member(user_id)
            user_name = target_user.display_name if target_user else f"User {user_id}"
            
            result = f"""USER PERMISSIONS REMOVED
User: {user_name} ({user_id})
Permission Level: 0 (Guest)
Removed by: {message.author.display_name}
Status: Permissions cleared"""
            
            await self.send_user_response(
                message.channel,
                " ".join(["user", "perms", "remove"] + args),
                result,
                message.author,
                True
            )
        except Exception as e:
            await self.send_user_response(
                message.channel,
                " ".join(["user", "perms", "remove"] + args),
                f"Error removing permissions: {str(e)}",
                message.author,
                False
            )
    
    async def list_users(self, message):
        """List all system users"""
        # Check permissions
        if not await self.check_permission(message.author, message.guild, 2):
            await self.send_user_response(
                message.channel,
                "user list",
                "Permission denied: You need Moderator (level 2) permissions",
                message.author,
                False
            )
            return
        
        try:
            users = await db_manager.get_all_system_users(message.guild.id)
            
            if not users:
                result = "No users in system\nUse 'user add <@user>' to add users"
            else:
                result = "SYSTEM USERS\n\n"
                for user_data in users:
                    discord_user = message.guild.get_member(user_data['discord_id'])
                    display_name = discord_user.display_name if discord_user else f"User {user_data['discord_id']}"
                    level_name = self.get_level_name(user_data.get('permission_level', 0))
                    
                    status = "Online" if user_data['discord_id'] in self.logged_in_users else "Offline"
                    
                    result += f"{display_name} ({user_data['username']}): Level {user_data.get('permission_level', 0)} ({level_name}) - {status}\n"
            
            await self.send_user_response(
                message.channel,
                "user list",
                result,
                message.author,
                True
            )
        except Exception as e:
            await self.send_user_response(
                message.channel,
                "user list",
                f"Error listing users: {str(e)}",
                message.author,
                False
            )
    
    async def set_password(self, message, args):
        """Set or change password"""
        # Determine target username
        if args:
            # Admin changing another user's password
            target_username = args[0]
            if not await self.check_permission(message.author, message.guild, 4):
                await self.send_user_response(
                    message.channel,
                    f"user passwd {target_username}",
                    "Permission denied: You need Senior Admin (level 4) permissions to change other users' passwords",
                    message.author,
                    False
                )
                return
        else:
            # User changing own password
            if message.author.id not in self.logged_in_users or not self.logged_in_users[message.author.id].get('logged_in'):
                await self.send_user_response(
                    message.channel,
                    "user passwd",
                    "You must be logged in to change your password\nUse 'login <username>' first",
                    message.author,
                    False
                )
                return
            target_username = self.logged_in_users[message.author.id]['username']
        
        # Prompt for new password
        await self.send_user_response(
            message.channel,
            f"user passwd {target_username}",
            f"New password for {target_username}:",
            message.author,
            True
        )
        
        # Wait for password input
        def check(m):
            return m.author == message.author and m.channel == message.channel
        
        try:
            password_msg = await self.bot.wait_for('message', check=check, timeout=30.0)
            await password_msg.delete()  # Delete password message immediately
            
            new_password = password_msg.content
            if len(new_password) < 4:
                await self.send_user_response(
                    message.channel,
                    f"user passwd {target_username}",
                    "Password too short. Minimum 4 characters required",
                    message.author,
                    False
                )
                return
            
            # Update password
            await db_manager.update_user_password(message.guild.id, target_username, new_password)
            
            result = f"""PASSWORD UPDATED
User: {target_username}
Changed by: {message.author.display_name}
Status: Password successfully changed"""
            
            await self.send_user_response(
                message.channel,
                f"user passwd {target_username}",
                result,
                message.author,
                True
            )
        
        except asyncio.TimeoutError:
            await self.send_user_response(
                message.channel,
                f"user passwd {target_username}",
                "Password change timeout: No password provided",
                message.author,
                False
            )
    
    async def check_permission(self, user, guild, required_level):
        """Check if user has required permission level"""
        try:
            # Check if logged in user has higher permissions
            if user.id in self.logged_in_users and self.logged_in_users[user.id].get('logged_in'):
                user_level = await db_manager.get_user_permission_level(guild.id, user.id)
                if user_level and user_level >= required_level:
                    return True
            
            # Check role permissions
            from cogs.modtools import ModTools
            server_groups_cog = self.bot.get_cog("ServerGroups")
            if server_groups_cog:
                user_level = await server_groups_cog.get_user_permission_level(user, guild)
                return user_level >= required_level
            
            return False
        except:
            return False
    
    def get_level_name(self, level):
        """Get permission level name"""
        level_names = {
            0: "Guest",
            1: "Supporter", 
            2: "Moderator",
            3: "Admin",
            4: "Senior Admin",
            5: "Super Admin"
        }
        return level_names.get(level, f"Level {level}")
    
    async def verify_password(self, guild_id, username, password):
        """Verify user password"""
        try:
            stored_password = await db_manager.get_user_password(guild_id, username)
            if not stored_password:
                return False
            
            # Simple password hashing (in production, use proper bcrypt)
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            return password_hash == stored_password
        except:
            return False

def setup(bot):
    bot.add_cog(UserManagement(bot))