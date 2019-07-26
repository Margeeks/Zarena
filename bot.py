#!/usr/bin/env python
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
from random import randint
import json
import asyncio
import time
import os
from os import listdir
from os.path import isfile, join
import aiohttp
import codecs
from datetime import datetime
import sys, traceback

def get_prefix(bot, message):
    prefixes = ['-']
    if not message.guild:
        return '?'
    return commands.when_mentioned_or(*prefixes)(bot, message)

cogs_dir = "cogs"
bot = commands.Bot(command_prefix=get_prefix, description='Rewrite Cog')
bot.launch_time = datetime.utcnow()
if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()

def cleanup_code(content):
    '''Automatically removes code blocks from the code.'''
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    return content.strip('` \n')


@bot.event 
async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game(name='VHackOS | -help'))
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Activity(name='VHackOS', type = discord.ActivityType.watching))
        await asyncio.sleep(30)       

@bot.event
async def on_ready():
    bot.loop.create_task(status_task()) 
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="introduce")
    embed = discord.Embed(title="Welcome " + f'{member.name}' + " to " + f'{member.guild}' + " !", description="First read the rules please...... Than I need your crew name, so type -crewlist to get list of crews & then -joincrew <crewname> to assign yourself in a crew....... It would be cool when you share the Link in your crew chat!!", color=0xeee657) 
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)


bot.remove_command('help')
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="vHackOS bot", description="A Very Nice bot. List of commands are:", color=0x03C03C)
    embed.add_field(name="Fun", value="hug | coinflip | greet | cookie | kill | slap | 8ball | face | tableflip | meme", inline=False)
    embed.add_field(name="Mod", value="mute | unmute | warn | kick | ban | purge", inline=False)
    embed.add_field(name="Utility", value="crewlist | joincrew | leavecrew ", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def rules(ctx):
    embed = discord.Embed(title="Welcome to vHackOS International server. This is unofficial server of vHackOS! ", color=0x007FFF)    
    embed.add_field(name=":bookmark:   VHackOS server rules ", value=":one: Insults are forbidden\n:two: No rasistic and pornographic content\n:three: Advertising for other vHack Discord groups is forbidden\n:four: Spamming is forbidden! Don't post any IP's\n:five: Dont use inappropriate nicknames\n:six: Don't use misplaced language")  
    embed.add_field(name=":white_check_mark:  Moderators and Owner have the task to look for Law and order, also to care an appropriate behavior\n",value="_")
    embed.add_field(name=":white_check_mark:  If you want to complain you about other players you can text the Owner Niko or the Moderator Flexua, Killultra & Steve\n",value="_")
    embed.add_field(name=":white_check_mark:  By a violation applies- The first 2 times you will get muted for 24h. By the 3 time you will get kicked. If make again a violation you get banned from the server", value=" Thank you for your attention and a lot of fun!")
    embed.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.send(embed=embed)

@bot.command()
async def crewlist(ctx):
    guild=ctx.guild
    embed = discord.Embed(title="List of available crews in {}".format(guild.name), colour=000000)
    embed.add_field(name="Lists", value="Rastafaricrew\nZenith\nLegendary\nTheAlienCrew\nReservoirDogs\nGemuesemafia\nGemuesegang\nJust4Fun\nChaosHackCrew\nWolfshack\nHackROM\nDoubleTrouble\nCryMad\nCannonballMC\nElhax\nDarkHackers\nfscociety\nQuantumEMP\nData_Rain\nHouseOfHelax\nUndefined\nIndefinido\nLifetimeEnemy\n500GrammHack\nGhostHack\nBirthofrage\nEmpire\nSalzcrew\nError404\nTheSpoofers\nTheWall\nHydraCrew\nHorizon\nPirati\n8bitCrew\nSpartans") 
    embed.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.send(embed=embed)
			  
@bot.command(aliases=['jc'])
async def joincrew(ctx, *, role: discord.Role = None):
        user=ctx.author
        if role is None:
            return await ctx.send("You haven't specified a crew to join! ")
        if role not in ctx.message.guild.roles:
            return await ctx.send("That crew doesn't exist. Please check the name properly from the list else ping any mod to create it.")
        if role not in ctx.message.author.roles:
            await user.add_roles(role)
            return await ctx.send("{} You have joined {} crew.".format(ctx.author.mention,role))
        if role in ctx.message.author.roles:
            return await ctx.send("{} You are already in {} crew, no need to join same crew twice.".format(ctx.author.mention,role))
        
@bot.command(aliases=['lc'])
async def leavecrew(ctx, *, role: discord.Role = None):
        user=ctx.author
        if role is None:
            return await ctx.send("You haven't specified a crew to  leave! ")
        if role in ctx.message.author.roles:
            await user.remove_roles(role)
            return await ctx.send("{} You have left {} crew.".format(ctx.author.mention,role))
        if role not in ctx.message.author.roles:
            return await ctx.send("{} You cannot leave the crew which you haven't joined.".format(ctx.author.mention))

@bot.command()
async def ping(ctx):
    embed=discord.Embed(title=None, description=':ping_pong: Ping: {} ms'.format(bot.latency * 1000), color=0x2874A6)
    await ctx.send(embed=embed)

@bot.command()
async def invite(ctx):
    await ctx.send("https://discord.gg/MKNdnXa")

@bot.command()
async def fb(ctx, *, msg):
    channel = bot.get_channel(477918661798264835)
    embed = discord.Embed(colour=ctx.author.colour)
    embed.add_field(name='User', value=ctx.author.name)
    embed.add_field(name='User ID', value=ctx.author.id, inline=True)
    embed.add_field(name='Server', value=ctx.guild.name, inline=True)
    embed.add_field(name='Server ID', value=ctx.guild.id, inline=True)
    embed.add_field(name='Message', value=msg)
    embed.add_field(name='Time', value=ctx.message.created_at)  
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_author(name=f'{ctx.message.author}'+" has submitted a feedback", icon_url=None or ctx.author.avatar_url)
    await channel.send(embed=embed)
    await ctx.send("Thank you!! Your feedback will be sent to the developer")

@bot.command(name="rep")
async def report(ctx,member: discord.Member=None,*,msg):
    channel = bot.get_channel(474636816692019211)
    if member is None:
        embed=discord.Embed(title="", description="You havent mentioned anyone to report!", color=0xff0000)          
        await ctx.send(embed=embed)
    else:  
        embed = discord.Embed(colour=ctx.author.colour)
        embed.add_field(name='Reported by - ', value=ctx.author.name)
        embed.add_field(name='Time', value=ctx.message.created_at)
        embed.add_field(name='Reason', value=msg)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_author(name=f'{ctx.message.author}'+" has been reported", icon_url=None or ctx.author.avatar_url)
        await channel.send(embed=embed)
        await ctx.send("Thank you!! Member had been reported")

@bot.command(name="sug")
async def suggest(ctx,*,msg):
    channel = bot.get_channel(474636816692019211)
    embed = discord.Embed(colour=ctx.author.colour)
    embed.add_field(name='Suggested by - ', value=ctx.author.name)
    embed.add_field(name='Time', value=ctx.message.created_at)
    embed.add_field(name='Suggestion', value=msg)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_author(name=f'{ctx.message.author}'+" has submitted a suggestion", icon_url=None or ctx.author.avatar_url)
    await channel.send(embed=embed)
    await ctx.send("Thank you for your suggestion !!")
			  
bot.run(os.getenv('TOKEN'))
