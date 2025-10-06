import discord
from discord.ext import commands
import re
from datetime import datetime, timedelta

class ModTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def send_mod_response(self, channel, command, result, user, success=True):
        current_time = discord.utils.utcnow().strftime("%H:%M:%S")
        terminal_output = f"```bash\n[{current_time}] {user.name}@modtools:~$ {command}\n{result}\n```"
        await channel.send(terminal_output)
    async def execute_kick(self, message, args):
        if len(args) < 2:
            await self.send_mod_response(
                message.channel, 
                " ".join(args), 
                "Usage: modtools kick <@user|user_id> [reason]", 
                message.author, 
                False
            )
            return
        
        if not message.author.guild_permissions.kick_members:
            await self.send_mod_response(
                message.channel, 
                " ".join(args), 
                "Permission denied: You need 'Kick Members' permission", 
                message.author, 
                False
            )
            return
        
        target_str = args[1]
        reason = " ".join(args[2:]) if len(args) > 2 else "No reason provided"
        
        try:
            user_id = None
            if target_str.startswith('<@') and target_str.endswith('>'):
                user_id = int(re.sub(r'[<@!>]', '', target_str))
            else:
                try:
                    user_id = int(target_str)
                except ValueError:
                    await self.send_mod_response(
                        message.channel, 
                        " ".join(args), 
                        f"User not found: {target_str}", 
                        message.author, 
                        False
                    )
                    return

            try:
                target_member = message.guild.get_member(user_id)
                if not target_member:
                    target_member = await message.guild.fetch_member(user_id)
                    
                if not target_member:
                    await self.send_mod_response(
                        message.channel, 
                        " ".join(args), 
                        f"Cannot kick {target_member.display_name}: User has higher/equal role", 
                        message.author, 
                        False
                    )
                    return
                
                if target_member.top_role >= message.author.top_role and message.author != message.guild.owner:
                    await self.send_mod_response(
                        message.channel, 
                        " ".join(args), 
                        "You cannot kick yourself", 
                        message.author, 
                        False
                    )
                    return
                
                if target_member == message.author:
                    await self.send_mod_response(
                        message.channel, 
                        " ".join(args), 
                        f"User not found: {target_str}", 
                        message.author, 
                        False
                    )
                    return
                
                if target_member.top_role >= message.guild.me.top_role:
                    await self.send_mod_response(
                        message.channel, 
                        " ".join(args), 
                        f"User not found: {target_str}", 
                        message.author, 
                        False
                    )
                    return
                
                await target_member.kick(reason=f"Kicked by {message.author} via LINCORD ModTools: {reason}")
                
                result = f"""KICK EXECUTED
Target: {target_member.display_name} ({target_member.id})
Reason: {reason}
Moderator: {message.author.display_name}
Status: User has been kicked from the server"""
                
                await self.send_mod_response(
                    message.channel, 
                    " ".join(args), 
                    result, 
                    message.author, 
                    True
                )
                
            except discord.Forbidden:
                await self.send_mod_response(
                    message.channel, 
                    " ".join(args), 
                    "Bot lacks permission to kick this user", 
                    message.author, 
                    False
                )
            except Exception as e:
                await self.send_mod_response(
                    message.channel, 
                    " ".join(args), 
                    f"Error during kick: {str(e)}", 
                    message.author, 
                    False
                )
        except Exception as e:
            print(f"ModTools kick error: {e}")
    
    async def execute_ban(self, message, args):
        if len(args) < 2:
            await self.send_mod_response(
                message.channel, 
                " ".join(args), 
                "Usage: modtools ban <@user|user_id> [reason]", 
                message.author, 
                False
            )
            return
        
        if not message.author.guild_permissions.ban_members:
            await self.send_mod_response(
                message.channel, 
                " ".join(args), 
                "Permission denied: You need 'Ban Members' permission", 
                message.author, 
                False
            )
            return
        
        target_str = args[1]
        reason = " ".join(args[2:]) if len(args) > 2 else "No reason provided"
        
        try:
            user_id = None
            if target_str.startswith('<@') and target_str.endswith('>'):
                user_id = int(re.sub(r'[<@!>]', '', target_str))
            else:
                try:
                    user_id = int(target_str)
                except ValueError:
                    await self.send_mod_response(
                        message.channel, 
                        " ".join(args), 
                        f"User not found: {target_str}", 
                        message.author, 
                        False
                    )
                    return
            
            try:
                target_member = message.guild.get_member(user_id)
                if not target_member:
                    try:
                        target_user = await self.bot.fetch_user(user_id)
                    except discord.NotFound:
                        await self.send_mod_response(
                            message.channel, 
                            " ".join(args), 
                            f"Cannot ban {target_member.display_name}: User has higher/equal role", 
                            message.author, 
                            False
                        )
                        return
                else:
                    target_user = target_member
                    
                    if target_member.top_role >= message.author.top_role and message.author != message.guild.owner:
                        await self.send_mod_response(
                            message.channel, 
                            " ".join(args), 
                            "You cannot ban yourself", 
                            message.author, 
                            False
                        )
                        return
                    
                    if target_member == message.author:
                        await self.send_mod_response(
                            message.channel, 
                            " ".join(args), 
                            f"User not found: {target_str}", 
                            message.author, 
                            False
                        )
                        return
                    
                    if target_member.top_role >= message.guild.me.top_role:
                        await self.send_mod_response(
                            message.channel, 
                            " ".join(args), 
                            f"User not found: {target_str}", 
                            message.author, 
                            False
                        )
                        return
                
                await message.guild.ban(
                    target_user, 
                    reason=f"Banned by {message.author} via LINCORD ModTools: {reason}",
                    delete_message_days=1
                )
                
                result = f"""BAN EXECUTED
Target: {target_user.display_name} ({target_user.id})
Reason: {reason}
Moderator: {message.author.display_name}
Status: User has been banned from the server"""
                
                await self.send_mod_response(
                    message.channel, 
                    " ".join(args), 
                    result, 
                    message.author, 
                    True
                )
                
            except discord.Forbidden:
                await self.send_mod_response(
                    message.channel, 
                    " ".join(args), 
                    "Bot lacks permission to ban this user", 
                    message.author, 
                    False
                )
            except Exception as e:
                await self.send_mod_response(
                    message.channel, 
                    " ".join(args), 
                    f"Error during ban: {str(e)}", 
                    message.author, 
                    False
                )
        except Exception as e:
            print(f"ModTools ban error: {e}")
    
    async def execute_timeout(self, message, args):
        if len(args) < 3:
            await self.send_mod_response(
                message.channel, 
                " ".join(args), 
                "Usage: modtools timeout <@user|user_id> <duration> [reason]\nDuration examples: 5m, 1h, 2d", 
                message.author, 
                False
            )
            return
        
        if not message.author.guild_permissions.moderate_members:
            await self.send_mod_response(
                message.channel, 
                " ".join(args), 
                "Permission denied: You need 'Moderate Members' permission", 
                message.author, 
                False
            )
            return
        
        target_str = args[1]
        duration_str = args[2]
        reason = " ".join(args[3:]) if len(args) > 3 else "No reason provided"
        
        duration_match = re.match(r'^(\d+)([mhd])$', duration_str.lower())
        if not duration_match:
            await self.send_mod_response(
                message.channel, 
                " ".join(args), 
                "Invalid duration format. Use: 5m, 1h, 2d", 
                message.author, 
                False
            )
            return
        
        amount = int(duration_match.group(1))
        unit = duration_match.group(2)
        
        if unit == 'm':
            duration = timedelta(minutes=amount)
        elif unit == 'h':
            duration = timedelta(hours=amount)
        elif unit == 'd':
            duration = timedelta(days=amount)
        
        try:
            user_id = None
            if target_str.startswith('<@') and target_str.endswith('>'):
                user_id = int(re.sub(r'[<@!>]', '', target_str))
            else:
                try:
                    user_id = int(target_str)
                except ValueError:
                    await self.send_mod_response(
                        message.channel, 
                        " ".join(args), 
                        f"User not found: {target_str}", 
                        message.author, 
                        False
                    )
                    return
            
            try:
                target_member = message.guild.get_member(user_id)
                if not target_member:
                    target_member = await message.guild.fetch_member(user_id)
                    
                if not target_member:
                    await self.send_mod_response(
                        message.channel, 
                        " ".join(args), 
                        f"User not found: {target_str}", 
                        message.author, 
                        False
                    )
                    return
                
                timeout_until = discord.utils.utcnow() + duration
                
                max_timeout = discord.utils.utcnow() + timedelta(days=28)
                if timeout_until > max_timeout:
                    await self.send_mod_response(
                        message.channel, 
                        " ".join(args), 
                        "Invalid duration format. Use numbers followed by m/h/d (e.g., 5m, 1h, 2d)", 
                        message.author, 
                        False
                    )
                    return
                
                await target_member.timeout(timeout_until, reason=f"Timed out by {message.author} via LINCORD ModTools: {reason}")
                
                result = f"""TIMEOUT EXECUTED
Target: {target_member.display_name} ({target_member.id})
Duration: {duration_str}
Until: {timeout_until.strftime('%Y-%m-%d %H:%M:%S UTC')}
Reason: {reason}
Moderator: {message.author.display_name}
Status: User has been timed out"""
                
                await self.send_mod_response(
                    message.channel, 
                    " ".join(args), 
                    result, 
                    message.author, 
                    True
                )
                
            except discord.Forbidden:
                await self.send_mod_response(
                    message.channel, 
                    " ".join(args), 
                    "Bot lacks permission to timeout this user", 
                    message.author, 
                    False
                )
            except Exception as e:
                await self.send_mod_response(
                    message.channel, 
                    " ".join(args), 
                    f"Error during timeout: {str(e)}", 
                    message.author, 
                    False
                )
        except Exception as e:
            print(f"ModTools timeout error: {e}")
    
    async def execute_clear(self, message, args):
        if len(args) < 2:
            await self.send_mod_response(
                message.channel, 
                " ".join(args), 
                "Usage: modtools clear <amount>", 
                message.author, 
                False
            )
            return

        if not message.author.guild_permissions.manage_messages:
            await self.send_mod_response(
                message.channel, 
                " ".join(args), 
                "Permission denied: You need 'Manage Messages' permission", 
                message.author, 
                False
            )
            return
        
        try:
            amount = int(args[1])
            if amount <= 0 or amount > 100:
                await self.send_mod_response(
                    message.channel, 
                    " ".join(args), 
                    "Amount must be between 1 and 100", 
                    message.author, 
                    False
                )
                return
        except ValueError:
            await self.send_mod_response(
                message.channel, 
                " ".join(args), 
                "Invalid amount. Must be a number between 1 and 100", 
                message.author, 
                False
            )
            return
        
        try:
            deleted = await message.channel.purge(limit=amount + 1)
            
            result = f"""CLEAR EXECUTED
Channel: {message.channel.name}
Messages deleted: {len(deleted) - 1}
Moderator: {message.author.display_name}
Status: Messages have been cleared"""
            
            await self.send_mod_response(
                message.channel, 
                " ".join(args), 
                result, 
                message.author, 
                True
            )
            
        except discord.Forbidden:
            await self.send_mod_response(
                message.channel, 
                " ".join(args), 
                "Bot lacks permission to delete messages", 
                message.author, 
                False
            )
        except Exception as e:
            await self.send_mod_response(
                message.channel, 
                " ".join(args), 
                f"Error during clear: {str(e)}", 
                message.author, 
                False
            )

def setup(bot):
    bot.add_cog(ModTools(bot))