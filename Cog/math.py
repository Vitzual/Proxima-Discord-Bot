import discord
import math
from discord.ext import commands, tasks

class Math(commands.Cog, name="Math"):
    """Basic math commands"""
    def __init__(self, bot):
        self.bot = bot

    # Basic math commands
    @commands.command()
    async def add(self, ctx, num1: float, num2: float):
        """Adds two numbers together"""
        await ctx.send(num1 + num2)

    @commands.command()
    async def subtract(self, ctx, num1: float, num2: float):
        """Subtract two numbers"""
        await ctx.send(num1 - num2)

    @commands.command()
    async def multiply(self, ctx, num1: float, num2: float):
        """Multiply two numbers together"""
        await ctx.send(num1 * num2)

    @commands.command()
    async def divide(self, ctx, num1: float, num2: float):
        """Divide two numbers"""
        await ctx.send(num1 / num2)

    @commands.command()
    async def power(self, ctx, num1: float, num2: float):
        """Takes number to power of other number"""
        await ctx.send(num1 ** num2)

    @commands.command()
    async def modulus(self, ctx, num1: float, num2: float):
        """Does modulus division between two numbers"""
        await ctx.send(num1 % num2)

    @commands.command()
    async def sqrt(self, ctx, num: float):
        """Calculates the square root of a number"""
        await ctx.send(math.sqrt(num))


def setup(bot):
    bot.add_cog(Math(bot))
