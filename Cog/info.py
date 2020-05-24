import discord
from discord.ext import commands, tasks


class Info(commands.Cog, name="Info"):
    """Informative commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def website(self, ctx):
        """Displays link to our website"""
        embed = discord.Embed(title="Our website", url="https://proximastudios.ca/", description="Click to go to our website", color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command()
    async def discord(self, ctx):
        """Displays link to our discord"""
        embed = discord.Embed(title="Our discord", url="https://discord.gg/ArBTCSC", description="Click to get a link to our discord", color=discord.Color.blue())
        await ctx.send(embed=embed)
        
    @commands.command()
    async def bot(self, ctx):
        """Displays link to bots github"""
        embed = discord.Embed(title="Bot code", url="https://github.com/Vitzual/proxima-bot", description="You can check out my code, it's open source!", color=discord.Color.blue())
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
