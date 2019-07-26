import discord
from discord.ext import commands
import aiohttp
import sys
import time
import googletrans
import functools

class utility:
    def __init__(self, bot):
	    self.bot = bot

		
    @commands.command()
    async def avatar(self, ctx, *, member: discord.Member = None):
       if member is None:
          embed=discord.Embed(title="No mention!", description="Please mention a user to view his profile!", color=0xff0000)
          await ctx.send(embed=embed)
       else:
          embed = discord.Embed(title=f"{member}'s profile picture", color=0xeee657)
          embed.set_image(url=member.avatar_url)
          await ctx.send(embed=embed)

    @commands.command()
    async def code(self, ctx, *, msg):
           """Write text in code format."""
           await ctx.message.delete()
           await ctx.send("```" + msg.replace("`", "") + "```")
       
    @commands.command()
    async def echo(self, ctx, *, content:str):
           await ctx.send(content)
           await ctx.message.delete()
		
    @commands.command()
    async def hello(self, ctx):
           """*hello
           A command that will respond with a random greeting.
           """
           choices = ('Hey!', 'Hello!', 'Hi!', 'Hallo!', 'Bonjour!', 'Hola!')
           await ctx.send(choice(choices))
    
    @commands.command(aliases=['platform'])
    async def plat(self,ctx):
           await ctx.send('Running on ' + sys.platform)
	
    @commands.command(name='members')
    async def membs(self, ctx):
        server = ctx.guild
        for member in server.members:
            await ctx.send(member)

    @commands.command(name='roles')
    async def rols(self, ctx):
        server = ctx.guild
        for role in server.roles:
            await ctx.send(role)

    @commands.command(name='member')
    async def mem(self, ctx):
        server = ctx.guild
        list = []
        for member in server.members:
            list.append(member.name)
        embed = discord.Embed(name =    'Members', description =    str(list) ,colour =    discord.Colour.green())
        await ctx.send(embed=embed)

    @commands.command(name='role')
    async def rol(self, ctx):
        server = ctx.guild
        list = []
        for role in server.roles:
            list.append(role.name)
        embed = discord.Embed(name =    'Roles', description =    str(list) ,colour =    discord.Colour.green())
        await ctx.send(embed=embed)

    @commands.command(name='pingme')
    async def pingme(self, ctx):
        embed=discord.Embed(description =    ctx.author.mention,colour =    discord.Colour.red())
        await ctx.send(embed=embed)

    @commands.command(name='translate')
    async def _translate(self, ctx, text, *, langs=""):
        def convert(s: str) -> dict:
            a = s.lower().split()
            res = {
                a[i]: a[i + 1]
                for i in range(len(a)) if a[i] in ("from", "to")
            }
            res["from"] = res.get("from") or "auto"
            res["to"] = res.get("to") or "en"
            return res

        try:
            langdict = convert(langs)
        except IndexError:
            raise commands.BadArgument("Invalid language format.")
        translator = googletrans.Translator()
        tmp = functools.partial(
            translator.translate,
            text,
            src=langdict["from"],
            dest=langdict["to"])
        try:
            async with ctx.typing():
                res = await self.bot.loop.run_in_executor(None, tmp)
        except ValueError as e:
            raise commands.BadArgument(e.args[0].capitalize())
        await ctx.send(res.text.replace("@", "@\u200b"))
	
def setup(bot):
    bot.add_cog(utility(bot))
