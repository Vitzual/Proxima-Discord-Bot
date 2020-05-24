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
    async def create(self, ctx, name):
        """Creates a new project in the discord"""
        guild = ctx.guild
        member = ctx.author
        username = ctx.message.author.name
        admin_role = get(guild.roles, name="Proxima Team")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
            admin_role: discord.PermissionOverwrite(read_messages=True)
        }
        username = username + "'s Projects"
        category = get(ctx.guild.categories, name=username)
        if category is not None and len(category.channels) >= 3:
            embed = discord.Embed(title="Slow down there cowboy!", description="You can only have 3 active projects at a time!", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            if category is None:
                await ctx.guild.create_category(username)
            category = get(ctx.guild.categories, name=username)
            channel = await guild.create_text_channel(name, overwrites=overwrites, category=category)
            embed = discord.Embed(title="Success!", description="Your project is ready to go!", color=discord.Color.blue())
            print(username,"has created a new project with the name",name)
            await ctx.send(embed=embed)
            username = ctx.message.author.name
            embed = discord.Embed(title="Welcome!", description=f"Hey {username}, welcome to your new project! Now\n"
                                                                f"that you're ready to go, lets find some team\n"
                                                                f"members and get this thing rolling!\n"
                                                                f"\n**How to start:** \n"
                                                                f"\t- Get the word out! Type `-search` to begin.\n"
                                                                f"\t- Invite people! Type `-inv [name]` to add them.\n"
                                                                f"\t- Start planning! Every great idea needs a plan.\n"
                                                                ,color=discord.Color.blue())
            await channel.send(embed=embed)

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

    @commands.has_role("Developer")
    @commands.command()
    async def finish(self, ctx, project):
        """Finishes a project"""
        def check(m):
            return m.author == ctx.author
        guild = ctx.guild
        username = ctx.author.display_name
        username = username + "'s Projects"
        category = get(ctx.guild.categories, name=username)
        found = False
        if category is None:
            embed = discord.Embed(title="Whoops!", description="You don't have any active projects!", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            for scan in category.channels:
                if scan.name == project:
                    channel = scan
                    found = True
                    embed = discord.Embed(title="Confirmation", description="Please type `confirm` to finish the project.\n\n**What this does:**\n\t- Deletes the project in your category\n\t- Adds project to completion board", color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    msg = await self.bot.wait_for('message', check=check)
                    if msg.content.lower() == "confirm": 
                        embed = discord.Embed(title="Project complete!", description="Congratulations on finishing your project!\n\n**Now what?**\n\t- Upload to the marketplace\n\t- Share it with others\n\t- Get engaged with your audience!", color=discord.Color.blue())
                        await ctx.send(embed=embed)
                        embed = discord.Embed(title="Warning!", description="This channel will be deleted in 1 minute!", color=discord.Color.red())
                        await channel.send(embed=embed)
                        await asyncio.sleep(30)
                        embed = discord.Embed(title="Warning!", description="This channel will be deleted in 30 seconds!", color=discord.Color.red())
                        await channel.send(embed=embed)
                        await asyncio.sleep(15)
                        embed = discord.Embed(title="Warning!", description="This channel will be deleted in 15 seconds!", color=discord.Color.red())
                        await channel.send(embed=embed)
                        await asyncio.sleep(10)
                        embed = discord.Embed(title="Warning!", description="This channel will be deleted in 5 seconds!", color=discord.Color.red())
                        await channel.send(embed=embed)
                        await asyncio.sleep(5)
                        await channel.delete()
                    else:
                        embed = discord.Embed(title="Confirmation failed!", description="You did not confirm correctly!", color=discord.Color.red())
                        await ctx.send(embed=embed)
            if found is False:
                embed = discord.Embed(title="Whoops!", description="You don't have a project with that name!", color=discord.Color.red())
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Developer(bot))