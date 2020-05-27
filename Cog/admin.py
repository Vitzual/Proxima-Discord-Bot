import discord
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands import Bot


class Admin(commands.Cog, name="Admin"):
    """Administrative commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role("Proxima Team")
    @commands.command()
    async def debug(self, ctx):
        """Enables or disables debugging mode"""
        embed = discord.Embed(title="Debugging disabled", description="This must be activated through console!", color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.has_role("Proxima Team")
    @commands.command(pass_context=True)
    async def clear(self, ctx, number: int):
        """Clears x amount of messages"""
        if number > 99:
            embed = discord.Embed(title="Oops!", description="A maximum of 99 messages can be cleared.", color=discord.Color.red())
            await ctx.send(embed=embed)
        elif number < 1:
            embed = discord.Embed(title="Oops!", description="A minimum of 1 message is needed", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            mgs = []
            async for x in ctx.channel.history(limit=number+1):
                mgs.append(x)
            await ctx.channel.delete_messages(mgs)
            embed = discord.Embed(title="Messages cleared!", description=f"Wiped {number} messages from this channel", color=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.has_role("Proxima Team")
    @commands.command(pass_context=True)
    async def add(self, ctx, name: discord.Member):
        """Force adds a user"""
        for scan in ctx.channel.members:
            if scan.id == name.id:
                embed = discord.Embed(title="Error", description=f"{name} is already in this channel", color=discord.Color.red())
                await ctx.send(embed=embed)
                return
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = True
        overwrite.read_messages = True
        overwrite.read_message_history = True
        await ctx.channel.set_permissions(name, overwrite=overwrite)
        embed = discord.Embed(title="User added", description=f"Force added {name} to channel", color=discord.Color.blue())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Admin(bot))
