# Import necessary library functions
import discord
import asyncio
from discord.ext import commands, tasks
from discord.utils import get
import json

class Community(commands.Cog, name="Community"):
    """Community commands"""
    def __init__(self, bot):
        self.bot = bot
    client = discord.Client()

    @commands.command()
    async def leave(self, ctx):
        """Leave a project you're in"""

        ###########################################
        ############## CONFIGURATION ##############
        ###########################################
        # You can change these for your own project
        COMMAND_ENABLED = True
        CONFIRMATION_WORD = "confirm"
        CONFIRMATION_PROMPT = True
        PROJECT_SUFFIX = "'s Project"
        DATABASE_FILE_NAME = "project-list"
        DATABASE_EXTENSION = ".json" # Dont change!
        ###########################################

        if COMMAND_ENABLED is False:
            embed = discord.Embed(title="Command disabled", description="Looks like this command is disabled!", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        project = ctx.channel
        category = project.category

        if PROJECT_SUFFIX not in project.category.name:
            embed = discord.Embed(title="Whoops!", description="Command must be executed in a project!", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
            
        if DATABASE_EXTENSION is not ".json":
            embed = discord.Embed(title="WARNING", description=f"**Invalid database extension set!**\nIt looks like this value was changed.\n\n**Error:** Database must use .json files!\n*Revert this change, and then reload the module.*", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        database = (DATABASE_FILE_NAME + DATABASE_EXTENSION)

        try:
            with open(database) as f:
                data = json.load(f)
        except Exception as ex:
            embed = discord.Embed(title="Database Error!",
                                description=f"**Error:** {ex}",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            for scan in data:
                if scan["user_id"] == ctx.author.id:
                    if scan["channelA"] == ctx.channel.id or scan["channelB"] == ctx.channel.id:
                        embed = discord.Embed(title="Whoops!",
                        description=f"**You can't leave your own project!**\nIf you want to end your project, type -finish",
                        color=discord.Color.red())
                        await ctx.send(embed=embed)
                        return

        def check(m):
            return m.author == ctx.author

        for scan in project.members:
            if scan.id == ctx.author.id:
                if CONFIRMATION_PROMPT is True:
                    embed = discord.Embed(title="Confirm", description=f"Please type `{CONFIRMATION_WORD}` to leave the project", color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    msg = await self.bot.wait_for('message', timeout=60.0, check=check)
                    if msg.content.lower() != CONFIRMATION_WORD: 
                        embed = discord.Embed(title="Confirmation failed!", description="You did not confirm correctly!", color=discord.Color.red())
                        await ctx.send(embed=embed)
                        return
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = False
                overwrite.read_messages = False
                overwrite.read_message_history = False
                for setperm in category.channels:
                    await setperm.set_permissions(ctx.author, overwrite=overwrite)
                embed = discord.Embed(title=f"{ctx.author.name} left!", color=discord.Color.red())
                msg = await project.send(embed=embed)  
                if ctx.channel.id == project.id:
                    embed = discord.Embed(title="Project left!", description=f"You left {ctx.author}'s project!", color=discord.Color.red())
                    msg = await ctx.author.send(embed=embed)  
                    return
                else:
                    embed = discord.Embed(title="Project left!", description=f"You left {ctx.author}'s project!", color=discord.Color.blue())
                    msg = await ctx.send(embed=embed)  
                    return

def setup(bot):
    bot.add_cog(Community(bot))