import discord
import asyncio
from discord.ext import commands, tasks
from discord.utils import get

class Developer(commands.Cog, name="Developer"):
    """Developer commands"""
    def __init__(self, bot):
        self.bot = bot

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
                                                    f"\n`-search [Role] [Desc]`\n"
                                                    f"\n`[Role]` **The role you're looking for**"
                                                    f"\nValid roles are developer, designer,\ncomposer, and tester.\n"
                                                    f"\n`[Desc]` **Description of the project**"
                                                    f"\nIt is recommended you also include\nwhat you're looking for from the role\nyou selected in the first argument.\n"
                                                    ,color=discord.Color.blue())
            await ctx.send(embed=embed)

        
def setup(bot):
    bot.add_cog(Developer(bot))
