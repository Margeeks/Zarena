import discord
import random
import asyncio
import json
from discord.ext import commands
import aiohttp

class fun:
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command()
    async def hug(self, ctx, *,member : discord.Member = None):
        if member is None:
            await ctx.send(ctx.message.author.mention + " has been hugged! 💘 ")
        else:
            if member.id == ctx.message.author.id:
                await ctx.send (ctx.message.author.mention + " hugged themselve because they are a loner 🤦 ")
            else:
                await ctx.send(member.mention + " was hugged by " + ctx.message.author.mention + " 💝 ")


    @commands.command(pass_context=True)
    async def coinflip(self, ctx):
        '''Select Random'''
        choice = random.randint(1,2)
        if choice == 1:
            await ctx.send("Tails")
        else:
            await ctx.send("Heads")

    @commands.command()
    async def greet(self, ctx):
         await ctx.send(":smiley: :wave: Hello, there!")
    
    @commands.command()
    async def hi(self, ctx):
        await ctx.send("Hello !")
        await ctx.message.delete()
        
    @commands.command()
    async def cat(self, ctx):
        await ctx.send("https://moderncat-wpengine.netdna-ssl.com/sites/default/files/images/uploads/ScienceKittens.gif")
        
    @commands.command(description='Lets see, what bot prefers')
    async def choose(self, ctx, *choices : str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))

    @commands.command()
    async def kill(self, ctx, *, member: discord.Member = None):
        if member is None:
            embed=discord.Embed(title="No one to kill!", description="You havent mentioned anyone to kill!", color=0xff0000)
            embed.set_thumbnail(url="http://i.imgur.com/6YToyEF.png")
            embed.set_footer(text = "I thought you are not enough stupid")
            await ctx.send(embed=embed)
        elif member.id == ctx.message.author.id:
            embed=discord.Embed(title="Call this number", description="1-800-784-2433", color=0xff0000)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/NHS-Logo.svg/1200px-NHS-Logo.svg.png")
            embed.set_image(url="http://4.bp.blogspot.com/-FL6mKTZOk94/UBb_9EuAYNI/AAAAAAAAOco/JWsTlyInMeQ/s400/Jean+Reno.gif")
            embed.set_footer(text="~~You are good~~")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Killed!", description="{} Was killed by {} OOF ".format(member.mention, ctx.message.author.name),color=0x00ff00)
            embed.set_image(url="https://media.giphy.com/media/kOA5F569qO4RG/giphy.gif")
            embed.set_footer(text= "RIP")
            await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, *, member: discord.Member = None):
        if member is None:
            embed=discord.Embed(title="No one to slap!", description="You havent mentioned anyone to slap!", color=0xff0000)
            embed.set_thumbnail(url="http://i.imgur.com/6YToyEF.png")
            embed.set_footer(text = "I thought you are not enough stupid")
            await ctx.send(embed=embed)
        elif member.id == ctx.message.author.id:
            embed=discord.Embed(title="Call this number", description="1-800-784-2433", color=0xff0000)
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/NHS-Logo.svg/1200px-NHS-Logo.svg.png")
            embed.set_image(url="https://media.giphy.com/media/pVi6sMBJhJ0E8/giphy.gif")
            embed.set_footer(text="~~You are good~~")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="slapped!", description="{} Was slapped by {} OOF ".format(member.mention, ctx.message.author.name),color=0x00ff00)
            embed.set_image(url="https://media.giphy.com/media/jLeyZWgtwgr2U/giphy.gif")
            embed.set_footer(text= "RIP")
            await ctx.send(embed=embed)

    
    
    @commands.command()
    async def face(self, ctx):
        faces=["¯\_(ツ)_/¯", "̿̿ ̿̿ ̿̿ ̿'̿'\̵͇̿̿\З= ( ▀ ͜͞ʖ▀) =Ε/̵͇̿̿/’̿’̿ ̿ ̿̿ ̿̿ ̿̿", "( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)", "ʕ•ᴥ•ʔ", "(▀̿Ĺ̯▀̿ ̿)", "(ง ͠° ͟ل͜ ͡°)ง", "༼ つ ◕_◕ ༽つ", "ಠ_ಠ", "(づ｡◕‿‿◕｡)づ", "̿'̿'\̵͇̿̿\З=( ͠° ͟ʖ ͡°)=Ε/̵͇̿̿/'̿̿ ̿ ̿ ̿ ̿ ̿", "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ ✧ﾟ･: *ヽ(◕ヮ◕ヽ)", "┬┴┬┴┤ ͜ʖ ͡°) ├┬┴┬┴", "( ͡°╭͜ʖ╮͡° )", "(͡ ͡° ͜ つ ͡͡°)", "(• ε •)", "(ง'̀-'́)ง", "(ಥ﹏ಥ)", "(ノಠ益ಠ)ノ彡┻━┻", "[̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲̅]", "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", "(☞ﾟ∀ﾟ)☞", "| (• ◡•)| (❍ᴥ❍ʋ)", "(◕‿◕✿)", "(ᵔᴥᵔ)", "(¬‿¬)", "(☞ﾟヮﾟ)☞ ☜(ﾟヮﾟ☜)", "(づ￣ ³￣)づ", "ლ(ಠ益ಠლ)", "ಠ╭╮ಠ", "̿ ̿ ̿'̿'\̵͇̿̿\з=(•_•)=ε/̵͇̿̿/'̿'̿ ̿", "(;´༎ຶД༎ຶ`)", "༼ つ  ͡° ͜ʖ ͡° ༽つ", "(╯°□°）╯︵ ┻━┻"]
        face=random.choice(faces)
        await ctx.send(face)

    @commands.command()
    async def tableflip(self, ctx):
        x = await ctx.send(content="┬─┬ノ( º _ ºノ)")
        await asyncio.sleep(1)
        await x.edit(content='(°-°)\\ ┬─┬')
        await asyncio.sleep(1)
        await x.edit(content='(╯°□°)╯    ]')
        await asyncio.sleep(0.2)
        await x.edit(content='(╯°□°)╯  ︵  ┻━┻')
      
    
    @commands.command()
    async def meme(self, ctx):
        """Pulls a random meme from r/me_irl"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.reddit.com/r/me_irl/random") as r:
                data = await r.json()
                await ctx.send(data[0]["data"]["children"][0]["data"]["url"])
     

    @commands.command()
    async def quotes(self, ctx):
        """*quotes
        A command that will return a random quotation.
        """
        self.session = aiohttp.ClientSession()
        params = {'method': 'getQuote', 'lang': 'en', 'format': 'json'}
        async with self.session.get('https://api.forismatic.com/api/1.0/', params=params) as response:
            data = await response.json()

            embed = discord.Embed(colour=discord.Colour.purple())
            embed.add_field(name=data['quoteText'], value=f"- {data['quoteAuthor']}")

            await ctx.send(embed=embed)
            
    @commands.command()
    async def repeat(self, ctx, amount: int, *, message):
        if amount <= 5:
            for i in range(amount):
                await ctx.send(message)     
        else:
            await ctx.send('Please use a number less than or equal to five.')
            
    @commands.command()
    async def reverse(self, ctx, *, message):
        message = message.split()
        await ctx.send(' '.join(reversed(message)))


def setup(bot):
    bot.add_cog(fun(bot))
