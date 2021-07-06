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
import asyncio


class mod:
    def __init__(self, bot):
        self.bot = bot
 
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def mute(self, ctx, user : discord.User, time = None):
        channel = discord.utils.get(user.guild.channels, name="logs")
        if time != None:
            time = int(time)
            t = time * 60
            await ctx.channel.set_permissions(user, send_messages=False)
            embed=discord.Embed(title="", description=f"Done, {user.mention} is now muted and will be unmuted after {time} minutes!", color=0xff0000)          
            await channel.send(embed=embed)
            await asyncio.sleep(t)
            await ctx.channel.set_permissions(user, send_messages=True)
        else:
            await ctx.channel.set_permissions(user, send_messages=False)
            embed=discord.Embed(title="", description=f"Done, {user.mention} is now permanently muted.", color=0xff0000)          
            await channel.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unmute(self, ctx, user: discord.Member):
        '''Unmute someone'''
        channel = discord.utils.get(user.guild.channels, name="logs")
        await ctx.channel.set_permissions(user, send_messages=True)
        embed=discord.Embed(title="", description=f"Done, {user.mention} is unmuted", color=0xff0000)          
        await channel.send(embed=embed)


    @commands.command(hidden=True)
    @commands.has_permissions(administrator = True)
    async def dm(self, ctx, user: discord.Member, *, message):
        """DM someone xD"""
        await user.send(str(message))
        await ctx.message.delete()            
        await ctx.send("It was at time. :white_check_mark: ")


    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def warn(self, ctx, user: discord.Member, *, reason):
        """Sends that warning."""
        channel = discord.utils.get(user.guild.channels, name="logs")
        embed = discord.Embed(color=0xf52338, title=f"WARNING From {ctx.author.guild.name}**.", description=f"{user.mention} has been warned")
        embed.add_field(name="Warned by", value=f"{ctx.author.name} ") 
        embed.add_field(name="Reason", value=f" {reason}")
        await channel.send(embed=embed)
        #await user.send(embed=embed)
        #await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user : discord.Member, *, reason = None):
        '''OFC kick anyone'''
        channel = discord.utils.get(user.guild.channels, name="logs")
        if reason != None:
            await ctx.send(f"Done, {user.mention} is kicked, reason = {reason} ")
            embed=discord.Embed(title="", description=f"Done, {user.mention} is kicked, reason = {reason} ", color=0xff0000)          
            await channel.send(embed=embed)
            embed=discord.Embed(title=f"Kicked From {ctx.author.guild.name}", description =f"You have been kicked from **{ctx.author.guild.name}** by **{ctx.message.author.name}**, Reason ==> **{reason}**!",  color=0xf52338)
            await user.send(embed=embed)
            await ctx.guild.kick(user, reason = reason)
        else:
            reason = "Unspecified"
            await ctx.send(f"Done, {user} is kicked, reason = Unspecified ")
            embed=discord.Embed(title="", description=f"Done, {user} is kicked, reason = Unspecified ", color=0xff0000)          
            await channel.send(embed=embed)
            embed=discord.Embed(title=f"Kicked From {ctx.author.guild.name}", description = f"You have been kicked from **{ctx.author.guild.name}** by **{ctx.message.author.name}**, Reason ==> **Not Specified**!", color=0xf52338)
            await user.send(embed=embed)
            await ctx.guild.kick(user, reason = reason)
            
        

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, user : discord.User, *, reason = None):
        channel = discord.utils.get(user.guild.channels, name="logs")
        if reason != None:
            await ctx.send(f"Done, {user} is banned, reason = {reason} ")
            embed=discord.Embed(title="", description=f"Done, {user} is banned, reason = {reason} ", color=0xff0000)          
            await channel.send(embed=embed)
            embed=discord.Embed(title=f"Banned From {ctx.author.guild.name}", description = f"You have been Banned from **{ctx.author.guild.name}** by **{ctx.message.author.name}**, Reason ==> **{reason}**!", color=0xf52338)
            await user.send(embed=embed)
            await ctx.guild.ban(user, reason = reason)
        else:
            await ctx.send(f"Done, {user} is banned, reason = {reason} ")
            embed=discord.Embed(title="", description=f"Done, {user} is banned, reason = {reason} ", color=0xff0000)          
            await channel.send(embed=embed)
            embed=discord.Embed(title=f"Banned From {ctx.author.guild.name}",description = f"You have been Banned from **{ctx.author.guild.name}** by **{ctx.message.author.name}**, Reason ==> **Not Specified**!", color=0xf52338)
            await user.send(embed=embed)
            await ctx.guild.ban(user, reason = "Unspecified")
    

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def purge(ctx,*, amount):
        if ctx.author.permissions_in(ctx.channel).manage_messages:
            try:
                amount = await ctx.channel.purge(limit=int(amount)+1)
                await ctx.channel.send(':white_check_mark: Deleted {} message(s)'.format(len(amount)-1))
            
            except discord.errors.Forbidden:
                await ctx.send("You don't have premissions to use this command.")
        else:
            await ctx.send("You don't have premissions to use this command.")

def setup(bot):
    bot.add_cog(mod(bot))
