"""
MIT License

Zarena Discord Bot
Copyright (c) 2021 itsbravestone

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import discord
from discord.ext import commands
import psutil
import time
import os
import datetime
from datetime import datetime, timedelta
from utils import repo, default
import sys
import inspect
import unicodedata
import logging
import json
from utils import checks, formats
from utils.paginator import HelpPaginator, CannotPaginate
from collections import OrderedDict, deque, Counter
from imports import utils
utils_log = logging.getLogger('utils')

class Info:

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.process = psutil.Process(os.getpid())
        self.launch_time = datetime.utcnow()
        bot.remove_command('help')

    def emoji(self, emoji):
        with open('data/emojis.json') as f:
            emojis = json.load(f)
            e = emojis[emoji]
        return self.bot.get_emoji(e)

    async def __error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)

    def get_bot_uptime(self, *, brief=False):
        now = datetime.datetime.utcnow()
        delta = now - self.bot.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if not brief:
            if days:
                fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
            else:
                fmt = '{h} hours, {m} minutes, and {s} seconds'
        else:
            fmt = '{h}h {m}m {s}s'
            if days:
                fmt = '{d}d ' + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    def get_uptime(self, *, brief=False):
        # bot.launch_time = datetime.utcnow()
        delta_uptime = datetime.utcnow() - self.launch_time
        (hours, remainder) = divmod(int(delta_uptime.total_seconds()), 3600)
        (minutes, seconds) = divmod(remainder, 60)
        (days, hours) = divmod(hours, 24)
        if (not brief):
            if days:
                fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
            else:
                fmt = '{h} hours, {m} minutes, and {s} seconds'
        else:
            fmt = '{h}h {m}m {s}s'
            if days:
                fmt = '{d}d ' + fmt
        return fmt.format(d=days, h=hours, m=minutes, s=seconds)


    @commands.command(aliases=['si', 'server'])
    async def serverinfo(self, ctx):
        """Shows info about the current server."""
        guild = ctx.guild
        guild_age = (ctx.message.created_at - guild.created_at).days
        created_at = f"Server created on {guild.created_at.strftime('%b %d %Y at %H:%M')}. That\'s over {guild_age} days ago!"
        color = discord.Color.green()
        online = (len([m for m in guild.members if m.status == discord.Status.online and not m.bot]))
        away = (len([m for m in guild.members if m.status == discord.Status.idle and not m.bot]))
        dnd = (len([m for m in guild.members if m.status == discord.Status.dnd and not m.bot]))
        offline = (len([m for m in guild.members if m.status == discord.Status.offline and not m.bot]))
        bots = (len([m for m in guild.members if m.bot]))
        tm=(len(guild.members))
        tm2=(len([m for m in guild.members if not m.bot]))
        om=(len([m for m in guild.members if m.status is not discord.Status.offline and not m.bot]))
        ds=f"{self.emoji('online')} {online}\n {self.emoji('idle')} {away}\n {self.emoji('dnd')} {dnd}\n {self.emoji('offline')} {offline}"
        
        em = discord.Embed(description=created_at, color=color)
        em.add_field(name='Owner', value=guild.owner)
        em.add_field(name='Total users', value=f"{tm}\nHumans - {tm2}| Bots - {bots}")
        em.add_field(name="User stats", value=f"Online - {om}\n{ds}")
        em.add_field(name='Text Channels', value=len(guild.text_channels))
        em.add_field(name='Voice Channels', value=len(guild.voice_channels))
        em.add_field(name='Roles', value=len(guild.roles))
        em.set_thumbnail(url=None or guild.icon_url)
        em.set_author(name=guild.name, icon_url=None or guild.icon_url)
        await ctx.send(embed=em)

    @commands.command(aliases=['ui', 'user'])
    async def userinfo(self, ctx, *,user: discord.Member = None):
        '''Get user info for yourself or someone in the guild'''
        user = user or ctx.message.author
        guild = ctx.message.guild
        top=user.top_role
        guild_owner = guild.owner
        avi = user.avatar_url
        roles = sorted(user.roles, key=lambda r: r.position)
        desc = "\n".join(
            (
                f" "
                + {
                    discord.Status.online: "Online",
                    discord.Status.idle: "idle",
                    discord.Status.dnd: "dnd",
                    discord.Status.offline: "Offline/Invisible",
                }.get(user.status, "On Mars"),
            )
        )
        desc3 = "\n".join(
            (
                f" "
                + {
                    discord.Status.online: "Online",
                    discord.Status.idle: "Away",
                    discord.Status.dnd: "Busy",
                    discord.Status.offline: "Offline/Invisible",
                }.get(user.status, "On Mars"),
            )
        )
        for role in roles:
            if str(role.color) != '#000000':
                color = role.color
        if 'color' not in locals():
            color = 0

        rolenames = ', '.join([r.name for r in roles if r != '@everyone']) or 'None'
        time = ctx.message.created_at
        desc2 = f'{user.name} is currently in {desc} mode.'
        member_number = sorted(guild.members, key=lambda m: m.joined_at).index(user) + 1
        if user is None:
            em=discord.Embed(title="No one to mention!", description="You haven't mentioned anyone to see his info!", color=0xff0000)
            await ctx.send(embed=em)
        else:
            em = discord.Embed(color=color, description=desc2, timestamp=time)
            em.add_field(name='Name', value=user.name),
            em.add_field(name='Member Number', value=member_number, inline=True),
            em.add_field(name="Status", value=desc3, inline=True),
            em.add_field(name=f'Bot:',value=f'{user.bot}',inline=True),
            em.add_field(name='Account Created', value=user.created_at.__format__('%A, %B %d, %Y')),
            em.add_field(name='Join Date', value=user.joined_at.__format__('%A, %B %d, %Y')),
            em.add_field(name="Highest role", value=top)
            em.add_field(name='Roles', value=rolenames)
            em.set_thumbnail(url=avi or None)
            await ctx.send(embed=em)

    @commands.command(aliases=['role'])
    async def roleinfo(self, ctx, *, rolename):
        '''Get information about a role. Case Sensitive!'''
        try:
            role = discord.utils.get(ctx.message.guild.roles, name=rolename)
        except:
            return await ctx.send(f"Role could not be found. The system IS case sensitive!")

        em = discord.Embed(description=f'Role ID: {str(role.id)}', color=role.color or discord.Color.green())
        em.title = role.name
        perms = ""
        if role.permissions.administrator:
            perms += "Administrator, "
        if role.permissions.create_instant_invite:
            perms += "Create Instant Invite, "
        if role.permissions.kick_members:
            perms += "Kick Members, "
        if role.permissions.ban_members:
            perms += "Ban Members, "
        if role.permissions.manage_channels:
            perms += "Manage Channels, "
        if role.permissions.manage_guild:
            perms += "Manage Guild, "
        if role.permissions.add_reactions:
            perms += "Add Reactions, "
        if role.permissions.view_audit_log:
            perms += "View Audit Log, "
        if role.permissions.read_messages:
            perms += "Read Messages, "
        if role.permissions.send_messages:
            perms += "Send Messages, "
        if role.permissions.send_tts_messages:
            perms += "Send TTS Messages, "
        if role.permissions.manage_messages:
            perms += "Manage Messages, "
        if role.permissions.embed_links:
            perms += "Embed Links, "
        if role.permissions.attach_files:
            perms += "Attach Files, "
        if role.permissions.read_message_history:
            perms += "Read Message History, "
        if role.permissions.mention_everyone:
            perms += "Mention Everyone, "
        if role.permissions.external_emojis:
            perms += "Use External Emojis, "
        if role.permissions.connect:
            perms += "Connect to Voice, "
        if role.permissions.speak:
            perms += "Speak, "
        if role.permissions.mute_members:
            perms += "Mute Members, "
        if role.permissions.deafen_members:
            perms += "Deafen Members, "
        if role.permissions.move_members:
            perms += "Move Members, "
        if role.permissions.use_voice_activation:
            perms += "Use Voice Activation, "
        if role.permissions.change_nickname:
            perms += "Change Nickname, "
        if role.permissions.manage_nicknames:
            perms += "Manage Nicknames, "
        if role.permissions.manage_roles:
            perms += "Manage Roles, "
        if role.permissions.manage_webhooks:
            perms += "Manage Webhooks, "
        if role.permissions.manage_emojis:
            perms += "Manage Emojis, "

        if perms is None:
            perms = "None"
        else:
            perms = perms.strip(", ")
            
        thing = str(role.created_at.__format__('%A, %B %d, %Y'))

        em.add_field(name='Hoisted', value=str(role.hoist))
        em.add_field(name='Position from bottom', value=str(role.position))
        em.add_field(name='Managed by Integration', value=str(role.managed))
        em.add_field(name='Mentionable', value=str(role.mentionable))
        em.add_field(name='People in this role', value=str(len(role.members)))
        em.set_footer(text=f'Created At: {thing}')
        await ctx.send(embed=em)
        
    def format_seconds(self,time_seconds):
   
        seconds = time_seconds
        hours = 0
        minutes = 0
        days = 0
        while seconds >= 60:
            if seconds >= 60 * 60 * 24:
                seconds -= 60 * 60 * 24
                days += 1
            elif seconds >= 60 * 60:
                seconds -= 60 * 60
                hours += 1
            elif seconds >= 60:
                seconds -= 60
                minutes += 1

        return f"{days}d {hours}h {minutes}m {seconds}s"    

    @commands.command(aliases=['info', 'stats'])
    async def about(self, ctx):
        """ About the bot """
        ramUsage = self.process.memory_full_info().rss / 1024**2
        
        plat=sys.platform
        uptime = self.get_uptime(brief=True)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        length=0
        for f in os.listdir(dir_path):
            if not f.endswith(".py"):
                continue
            else:
                with open(dir_path+"/"+f , 'r', encoding="utf8") as b:
                    lines = b.readlines()
                    length+=len(lines)
        embed = discord.Embed(colour=ctx.me.top_role.colour)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(
            name=f"Developer{'' if len(self.config.owners) == 1 else 's'}",
            value=', '.join([str(self.bot.get_user(x)) for x in self.config.owners]),
            inline=True)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(name="Platform", value=plat, inline=True)
        embed.add_field(name="Commands loaded", value=len([x.name for x in self.bot.commands]), inline=True)
        embed.add_field(name="Servers", value=len(ctx.bot.guilds), inline=True)
        embed.add_field(name="RAM Usage", value=f"{ramUsage:.2f} MB", inline=True)
        embed.add_field(name="CPU Usage", value=f"{psutil.cpu_percent()}% CPU", inline=True)
        embed.add_field(name="Lines of Code",value = length)
        embed.add_field(name='Uptime', value=uptime)   
        embed.set_footer(text='Made with discord.py', icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(content=f"ℹ About **{ctx.bot.user}** | **{repo.version}**", embed=embed)

    @commands.command(brief = "shows the amount of users in the server")
    async def membercount(self, ctx):
        bots = 0
        members = 0
        total = 0
        for x in ctx.guild.members:
            if x.bot == True:
                bots += 1
                total += 1
            else:
                members += 1
                total += 1
        embed = discord.Embed(color = 0x2c7cff, title = f"Server Member Count")
        embed.add_field(name = "User Count", value = f'{members}', inline = True)
        embed.add_field(name = "Bot Count", value = f'{bots}', inline = True)
        embed.add_field(name = "Total", value = f'{total}', inline = True)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Info(bot))
