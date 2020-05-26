# Import necessary library functions
import discord
import asyncio
from discord.ext import commands, tasks
from discord.utils import get
import json

class Developer(commands.Cog, name="Developer"):
    """Developer commands"""
    def __init__(self, bot):
        self.bot = bot
    client = discord.Client()

    # Command "-create [Name]"
    @commands.has_role("Verified Developer")
    @commands.command()
    async def create(self, ctx, name):
        """Creates a new project in the discord"""

        ###########################################
        ############## CONFIGURATION ##############
        ###########################################
        # You can change these for your own project
        COMMAND_ENABLED = True
        ADMIN_ROLE = "Proxima Team"
        MAX_CHANNELS = 3
        MAX_CHANNELS_CHECK = True
        DUPLICATE_NAME_CHECK = True
        BLACKLIST_FILTER = True
        BLACKLIST_WORDS = ["example1", "example2"]
        ###########################################

        if COMMAND_ENABLED is False:
            discord.Embed(title="Command disabled", description="Looks like this command is disabled!", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if MAX_CHANNELS_CHECK and category is not None and len(category.channels) >= MAX_CHANNELS:
            embed = discord.Embed(title="Slow down there cowboy!", description=f"You can only have {MAX_CHANNELS} active projects at a time!", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if DUPLICATE_NAME_CHECK and category is not None:
            category = get(ctx.guild.categories, name=username)
            for scan in category.channels:
                if scan.name == name:
                    embed = discord.Embed(title="Whoops!", description="You already have a project with that name!", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    valid = False
            return

        if BLACKLIST_FILTER and name.lower in BLACKLIST_WORDS:
            embed = discord.Embed(title="Woah there!", description="Your project contained profanity!\n\n**Reminder:**\n- No projects with vulgar names\n- Projects must be child friendly", color=discord.Color.red())
            await ctx.send(embed=embed)
            valid = False
            return

        # Grabs guild, member, username, and admin role and then sets permissions for new project channels
        guild = ctx.guild
        member = ctx.author
        username = ctx.message.author.name
        admin_role = get(guild.roles, name=ADMIN_ROLE)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
            admin_role: discord.PermissionOverwrite(read_messages=True)
        }
        username = username + "'s Projects"
        category = get(ctx.guild.categories, name=username)
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

    @commands.has_role("Verified Developer")
    @commands.command()
    async def finish(self, ctx, project):
        """Finishes a project"""

        ###########################################
        ############## CONFIGURATION ##############
        ###########################################
        # You can change these for your own project
        COMMAND_ENABLED = True
        CONFIRMATION_WORD = "confirm"
        CONFIRMATION_PROMPT = True
        PROJECT_DELETE_COUNTDOWN = True
        COUNTDOWN_TIME = 60
        ###########################################

        if COMMAND_ENABLED is False:
            discord.Embed(title="Command disabled", description="Looks like this command is disabled!", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if COUNTDOWN_TIME < 60 and PROJECT_DELETE_COUNTDOWN is True:
            embed = discord.Embed(title="WARNING", description=f"**Invalid countdown time set!**\nIt looks like this value was changed.\n\n**Time entered:** {COUNTDOWN_TIME} seconds\n**Error:** Value must be greater then 60\n\n*Revert this change, and then reload the module.*", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        def check(m):
            return m.author == ctx.author
        guild = ctx.guild
        username = ctx.author.display_name
        username = username + "'s Projects"
        category = get(ctx.guild.categories, name=username)
        found = False
        confirmation_passed = True
        if category is None:
            embed = discord.Embed(title="Whoops!", description="You don't have any active projects!", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            for scan in category.channels:
                if scan.name == project:
                    channel = scan
                    found = True
                    if CONFIRMATION_PROMPT is True:
                        confirmation_passed = False
                        embed = discord.Embed(title="Confirmation", description=f"Please type `{CONFIRMATION_WORD}` to finish the project.\n\n**What this does:**\n\t- Deletes the project in your category\n\t- Adds project to completion board", color=discord.Color.blue())
                        await ctx.send(embed=embed)
                        msg = await self.bot.wait_for('message', check=check)
                        if msg.content.lower() == CONFIRMATION_WORD:
                            confirmation_passed = True
                        else:
                            embed = discord.Embed(title="Confirmation failed!", description="You did not confirm correctly!", color=discord.Color.red())
                            await ctx.send(embed=embed)
                    elif PROJECT_DELETE_COUNTDOWN is True:
                        await ctx.send(embed=embed)
                        embed = discord.Embed(title="Warning!", description=f"This channel will be deleted in {COUNTDOWN_TIME} seconds!", color=discord.Color.red())
                        await channel.send(embed=embed)
                        await asyncio.sleep(COUNTDOWN_TIME-30)
                        embed = discord.Embed(title="Warning!", description="This channel will be deleted in 30 seconds!", color=discord.Color.red())
                        await channel.send(embed=embed)
                        await asyncio.sleep(15)
                        embed = discord.Embed(title="Warning!", description="This channel will be deleted in 15 seconds!", color=discord.Color.red())
                        await channel.send(embed=embed)
                        await asyncio.sleep(10)
                        embed = discord.Embed(title="Warning!", description="This channel will be deleted in 5 seconds!", color=discord.Color.red())
                        await channel.send(embed=embed)
                        await asyncio.sleep(5)
                    if confirmation_passed is True:
                        embed = discord.Embed(title=":confetti_ball: Project complete! :confetti_ball:", description="Congratulations on finishing your project!\n\n**Now what?**\n\t- Upload to the marketplace\n\t- Share it with others\n\t- Get engaged with your audience!", color=discord.Color.blue())
                        await ctx.send(embed=embed)
                        category = get(ctx.guild.categories, name=username)
                        await channel.delete()
                        if len(category.channels) == 1:
                            await category.delete()
            if found is False:
                embed = discord.Embed(title="Whoops!", description="You don't have a project with that name!", color=discord.Color.red())
                await ctx.send(embed=embed)

    @commands.has_role("Verified Developer")
    @commands.command()
    async def toggle(self, ctx):
        """Opt-in or opt-out of receiving invites"""

        ###########################################
        ############## CONFIGURATION ##############
        ###########################################
        # You can change these for your own project
        COMMAND_ENABLED = True
        DATABASE_FILE_NAME = "opt-out"
        DATABASE_EXTENSION = ".json" # Dont change!
        ###########################################

        if COMMAND_ENABLED is False:
            embed = discord.Embed(title="Command disabled", description="Looks like this command is disabled!", color=discord.Color.red())
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
            i = 0
            for user in data:
                if user["user_id"] == ctx.author.id:
                    del data[i]
                    with open(database, "w") as f:
                        json.dump(data, f, indent=2)
                    embed = discord.Embed(title="You're in!",
                                        description="You have opted back into receiving invites!",
                                        color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    return
                i += 1
            new_user = {
                "user_id": ctx.author.id
            }
            data.append(new_user)
            with open(database, "w") as f:
                json.dump(data, f, indent=2)
            embed = discord.Embed(title="You're out!",
                                description="You have opted out of receiving invites!",
                                color=discord.Color.blue())
            await ctx.send(embed=embed)
            return

    @commands.has_role("Verified Developer")
    @commands.command()
    async def desc(self, ctx, name, *, description: str):
        """Changes the description of your project"""

        ###########################################
        ############## CONFIGURATION ##############
        ###########################################
        # You can change these for your own project
        COMMAND_ENABLED = True
        BLACKLIST_FILTER = True
        BLACKLIST_WORDS = ["example1", "example2"]
        ###########################################

        if COMMAND_ENABLED is False:
            embed = discord.Embed(title="Command disabled", description="Looks like this command is disabled!", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        elif BLACKLIST_FILTER and [a for a in BLACKLIST_WORDS if(a in description)]:
            embed = discord.Embed(title="Woah there!", description="Your description contained profanity!\n\n**Reminder:**\n- No descriptions with vulgar names\n- Descriptions must be child friendly", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        username = ctx.author.display_name + "'s Projects"
        category = get(ctx.guild.categories, name=username)
        found = False
        if category is None:
            embed = discord.Embed(title="Whoops!", description="You don't have any active projects!", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            for scan in category.channels:
                if scan.name == name:
                    await scan.edit(topic=description)
                    scan = scan.name.capitalize()
                    embed = discord.Embed(title=f"Success!",
                                        description=f"**{scan}'s description is now:** \n{description}",
                                        color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    found = True
        if found is False:
            embed = discord.Embed(title="Whoops!", description="You don't have a project with that name!", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.has_role("Verified Developer")
    @commands.command()
    async def search(self, ctx):
        """This feature is still in development"""
        guild = ctx.guild
        username = ctx.message.author.name
        username = username + "'s Projects"
        category = get(ctx.guild.categories, name=username)
        if category is None:
            embed = discord.Embed(title="Whoops!",
                                  description="You need to have an active project before starting a team search!",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Starting a search", description=f"Ready to start searching? Here's how\n"
                                                                         f"to start an active search...\n"
                                                                         f"\n`-search [Role]`\n"
                                                                         f"\n`[Role]` **The role you're looking for**"
                                                                         f"\nValid roles are developer, designer,\ncomposer, and tester.\n"
                                                                         f"\n**Remember** Set a description before\nstarting an active search with `-desc`\nso people know what the project is!"
                                  , color=discord.Color.blue())
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Developer(bot))