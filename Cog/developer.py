# Import necessary library functions
import discord
import asyncio
from discord.ext import commands, tasks
from discord.utils import get

class Developer(commands.Cog, name="Developer"):
    """Developer commands"""
    def __init__(self, bot):
        self.bot = bot
    client = discord.Client()

    @commands.has_role("Developer")
    @commands.command()
    async def search(self, ctx):
        """Starts an active team search"""
        guild = ctx.guild
        username = ctx.message.author.name
        username = username + "'s Projects"
        category = get(ctx.guild.categories, name=username)
        if category is None:
            embed = discord.Embed(title="Whoops!", description="You need to have an active project before starting a team search!", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Starting a search", description=f"Ready to start searching? Here's how\n"
                                                    f"to start an active search...\n"
                                                    f"\n`-search [Role]`\n"
                                                    f"\n`[Role]` **The role you're looking for**"
                                                    f"\nValid roles are developer, designer,\ncomposer, and tester.\n"
                                                    f"\n**Remember** Set a description before\nstarting an active search with `-desc`\nso people know what the project is!"
                                                    ,color=discord.Color.blue())
            await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Developer(bot))