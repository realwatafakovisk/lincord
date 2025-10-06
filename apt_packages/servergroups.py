import discord
from discord.ext import commands
import asyncio
from database import db_manager

class ServerGroups(commands.Cog):
    """Server groups and permission management system"""
    
    def __init__(self, bot):
        self.bot = bot
        self.permission_levels = {
            1: "Supporter",
            2: "Moderator", 
            3: "Admin",
            4: "Senior Admin",
            5: "Super Admin"
        }
    
    async def send_groups_response(self, channel, command, result, user, success=True):
        """Send server-groups response in terminal style"""
        current_time = discord.utils.utcnow().strftime("%H:%M:%S")
        terminal_output = f"```bash\n[{current_time}] {user.name}@groups:~$ {command}\n{result}\n```"
        await channel.send(terminal_output)
    
    async def execute_groups(self, message, args):
        """Execute groups commands"""
        if len(args) < 2:
            await self.send_groups_response(
                message.channel,
                " ".join(args),
                "Usage: groups <command> [options]\n\nCommands:\n  role add <@role> <level>  - Add role with permission level (1-5)\n  role remove <@role>       - Remove role from groups\n  role list                 - List all configured roles\n  info                      - Show permission levels",
                message.author,
                False
            )
            return
        
        subcmd = args[1].lower()
        
        if subcmd == "role":
            await self.handle_role_command(message, args[2:])
        elif subcmd == "info":
            await self.show_permission_info(message)
        else:
            await self.send_groups_response(
                message.channel,
                " ".join(args),
                f"Unknown command: {subcmd}\nUse 'groups' without arguments for help",
                message.author,
                False
            )
    
    async def handle_role_command(self, message, args):
        """Handle role subcommands"""
        if not args:
            await self.send_groups_response(
                message.channel,
                "groups role",
                "Usage: groups role <add|remove|list> [options]",
                message.author,
                False
            )
            return
        
        action = args[0].lower()
        
        if action == "add":
            await self.add_role_permission(message, args[1:])
        elif action == "remove":
            await self.remove_role_permission(message, args[1:])
        elif action == "list":
            await self.list_role_permissions(message)
        else:
            await self.send_groups_response(
                message.channel,
                f"groups role {action}",
                f"Unknown action: {action}\nUse: add, remove, or list",
                message.author,
                False
            )
    
    async def add_role_permission(self, message, args):
        """Add role with permission level"""
        if len(args) < 2:
            await self.send_groups_response(
                message.channel,
                "groups role add",
                "Usage: groups role add <@role> <level>\nLevel: 1-5 (1=Supporter, 5=Super Admin)",
                message.author,
                False
            )
            return
        
        # Check if user has permission (only Super Admin can manage groups)
        user_level = await self.get_user_permission_level(message.author, message.guild)
        if user_level < 5:
            await self.send_groups_response(
                message.channel,
                " ".join(["groups", "role", "add"] + args),
                "Permission denied: You need Super Admin (level 5) permissions",
                message.author,
                False
            )
            return
        
        role_mention = args[0]
        try:
            level = int(args[1])
            if level < 1 or level > 5:
                raise ValueError("Invalid level")
        except ValueError:
            await self.send_groups_response(
                message.channel,
                " ".join(["groups", "role", "add"] + args),
                "Invalid permission level. Use 1-5",
                message.author,
                False
            )
            return
        
        # Extract role ID
        if role_mention.startswith('<@&') and role_mention.endswith('>'):
            role_id = int(role_mention[3:-1])
        else:
            await self.send_groups_response(
                message.channel,
                " ".join(["groups", "role", "add"] + args),
                "Invalid role format. Use @role mention",
                message.author,
                False
            )
            return
        
        # Get role object
        role = message.guild.get_role(role_id)
        if not role:
            await self.send_groups_response(
                message.channel,
                " ".join(["groups", "role", "add"] + args),
                f"Role not found: {role_mention}",
                message.author,
                False
            )
            return
        
        # Add to database
        try:
            await db_manager.add_role_permission(message.guild.id, role_id, level)
            level_name = self.permission_levels.get(level, f"Level {level}")
            
            result = f"""ROLE PERMISSION ADDED
Role: {role.name} ({role_id})
Permission Level: {level} ({level_name})
Added by: {message.author.display_name}
Status: Role configured successfully"""
            
            await self.send_groups_response(
                message.channel,
                " ".join(["groups", "role", "add"] + args),
                result,
                message.author,
                True
            )
        except Exception as e:
            await self.send_groups_response(
                message.channel,
                " ".join(["groups", "role", "add"] + args),
                f"Error adding role permission: {str(e)}",
                message.author,
                False
            )
    
    async def remove_role_permission(self, message, args):
        """Remove role permission"""
        if not args:
            await self.send_groups_response(
                message.channel,
                "groups role remove",
                "Usage: groups role remove <@role>",
                message.author,
                False
            )
            return
        
        # Check permissions
        user_level = await self.get_user_permission_level(message.author, message.guild)
        if user_level < 5:
            await self.send_groups_response(
                message.channel,
                " ".join(["groups", "role", "remove"] + args),
                "Permission denied: You need Super Admin (level 5) permissions",
                message.author,
                False
            )
            return
        
        role_mention = args[0]
        
        # Extract role ID
        if role_mention.startswith('<@&') and role_mention.endswith('>'):
            role_id = int(role_mention[3:-1])
        else:
            await self.send_groups_response(
                message.channel,
                " ".join(["groups", "role", "remove"] + args),
                "Invalid role format. Use @role mention",
                message.author,
                False
            )
            return
        
        try:
            await db_manager.remove_role_permission(message.guild.id, role_id)
            role = message.guild.get_role(role_id)
            role_name = role.name if role else f"Role {role_id}"
            
            result = f"""ROLE PERMISSION REMOVED
Role: {role_name} ({role_id})
Removed by: {message.author.display_name}
Status: Role permissions cleared"""
            
            await self.send_groups_response(
                message.channel,
                " ".join(["groups", "role", "remove"] + args),
                result,
                message.author,
                True
            )
        except Exception as e:
            await self.send_groups_response(
                message.channel,
                " ".join(["groups", "role", "remove"] + args),
                f"Error removing role permission: {str(e)}",
                message.author,
                False
            )
    
    async def list_role_permissions(self, message):
        """List all role permissions"""
        try:
            roles = await db_manager.get_server_role_permissions(message.guild.id)
            
            if not roles:
                result = "No role permissions configured\nUse 'groups role add <@role> <level>' to add roles"
            else:
                result = "CONFIGURED ROLE PERMISSIONS\n\n"
                for role_id, level in roles.items():
                    role = message.guild.get_role(int(role_id))
                    role_name = role.name if role else f"Unknown Role ({role_id})"
                    level_name = self.permission_levels.get(level, f"Level {level}")
                    result += f"{role_name}: Level {level} ({level_name})\n"
            
            await self.send_groups_response(
                message.channel,
                "groups role list",
                result,
                message.author,
                True
            )
        except Exception as e:
            await self.send_groups_response(
                message.channel,
                "groups role list",
                f"Error listing roles: {str(e)}",
                message.author,
                False
            )
    
    async def show_permission_info(self, message):
        """Show permission level information"""
        result = """PERMISSION LEVELS

Level 1 (Supporter):     Basic user management, timeouts
Level 2 (Moderator):     User management, kicks, message moderation  
Level 3 (Admin):         Full moderation, server configuration
Level 4 (Senior Admin):  Advanced management, system configuration
Level 5 (Super Admin):   Full system access, permission management

Use 'groups role add <@role> <level>' to assign levels to roles"""
        
        await self.send_groups_response(
            message.channel,
            "groups info",
            result,
            message.author,
            True
        )
    
    async def get_user_permission_level(self, user, guild):
        """Get user's highest permission level"""
        try:
            # Check user-specific permissions first
            user_level = await db_manager.get_user_permission_level(guild.id, user.id)
            if user_level:
                return user_level
            
            # Check role permissions
            role_permissions = await db_manager.get_server_role_permissions(guild.id)
            if not role_permissions:
                return 0  # Guest level
            
            highest_level = 0
            for role in user.roles:
                if str(role.id) in role_permissions:
                    level = role_permissions[str(role.id)]
                    if level > highest_level:
                        highest_level = level
            
            return highest_level
        except:
            return 0  # Guest level on error

def setup(bot):
    bot.add_cog(ServerGroups(bot))