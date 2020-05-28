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

    @commands.has_role("Verified Developer")
    @commands.command(aliases=["new", "start"])
    async def create(self, ctx):
        """Creates a new project in the discord"""

        ###########################################
        ############## CONFIGURATION ##############
        ###########################################
        # You can change these for your own project
        COMMAND_ENABLED = True
        DATABASE_FILE_NAME = "project-list"
        DATABASE_EXTENSION = ".json" # Dont change!
        ADMIN_ROLE = "Proxima Team"
        ###########################################

        if COMMAND_ENABLED is False:
            discord.Embed(title="Command disabled", description="Looks like this command is disabled!", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if DATABASE_EXTENSION is not ".json":
            embed = discord.Embed(title="WARNING", description=f"**Invalid database extension set!**\nIt looks like this value was changed.\n\n**Error:** Database must use .json files!\n*Revert this change, and then reload the module.*", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        database = (DATABASE_FILE_NAME + DATABASE_EXTENSION)
        user_threshold = 3

        try:
            with open(database) as f:
                data = json.load(f)
        except Exception as ex:
            embed = discord.Embed(title="Database Error!",
                                description=f"**Error:** {ex}",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            while user_threshold > 1:
                user_threshold -= 1
                i = 0
                for user in data:
                    if user["user_id"] == ctx.author.id:
                        try:
                            projectID = user["project_owned"]

                        except KeyError:
                            try:
                                del data[i]
                                with open(database, "w") as f:
                                    json.dump(data, f, indent=2)
                                guild = ctx.guild
                                admin_role = get(guild.roles, name=ADMIN_ROLE)
                                overwrites = {
                                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                    guild.me: discord.PermissionOverwrite(read_messages=True),
                                    ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
                                    admin_role: discord.PermissionOverwrite(read_messages=True)
                                }
                                project_name = ctx.author.name+"'s Project"
                                await ctx.guild.create_category(project_name)
                                category = get(ctx.guild.categories, name=project_name)
                                await guild.create_text_channel("updates", overwrites=overwrites, category=category)
                                channel = await guild.create_text_channel("discussion", overwrites=overwrites, category=category)
                                embed = discord.Embed(title="Success!", description="Your project is ready to go!", color=discord.Color.blue())
                                await ctx.send(embed=embed)
                                embed = discord.Embed(title="Welcome!", description=f"Hey {ctx.message.author.name}, welcome to your new project! Now\n"
                                                                                    f"that you're ready to go, lets find some team\n"
                                                                                    f"members and get this thing rolling!\n"
                                                                                    f"\n**How to start:** \n"
                                                                                    f"\t- Get the word out! Type `-search` to begin.\n"
                                                                                    f"\t- Invite people! Type `-inv [name]` to add them.\n"
                                                                                    f"\t- Start planning! Every great idea needs a plan.\n"
                                                                                    ,color=discord.Color.blue())
                                await channel.send(embed=embed)
                                new_project = {
                                    "user_id": ctx.author.id,
                                    "project_owned": category.id
                                }
                                data.append(new_project)
                                with open(database, "w") as f:
                                    json.dump(data, f, indent=2)
                                return
                            except Exception as ex:
                                embed = discord.Embed(title="Database Error!",
                                                    description=f"**Error:** {ex}",
                                                    color=discord.Color.red())
                                await ctx.send(embed=embed)
                                return
                        else:
                            embed = discord.Embed(title="Whoops!", description="You already own a project!", color=discord.Color.red())
                            await ctx.send(embed=embed)
                            return
                    i += 1
                new_user = {
                    "user_id": ctx.author.id
                }
                data.append(new_user)
                with open(database, "w") as f:
                    json.dump(data, f, indent=2)

    @commands.has_role("Verified Developer")
    @commands.command()
    async def finish(self, ctx):
        """Finishes a project"""

        ###########################################
        ############## CONFIGURATION ##############
        ###########################################
        # You can change these for your own project
        COMMAND_ENABLED = True
        CONFIRMATION_WORD = "confirm" 
        CONFIRMATION_PROMPT = True 
        DATABASE_FILE_NAME = "project-list"
        DATABASE_EXTENSION = ".json" # Dont change!
        ###########################################

        if COMMAND_ENABLED is False:
            discord.Embed(title="Command disabled", description="Looks like this command is disabled!", color=discord.Color.red())
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
            def check(m):
                return m.author == ctx.author
            i = 0
            for user in data:
                if user["user_id"] == ctx.author.id:
                    try:
                        projectID = user["project_owned"]
                    except KeyError:
                        pass
                    else:
                        if CONFIRMATION_PROMPT is True:
                            embed = discord.Embed(title="Confirmation", description=f"Please type `{CONFIRMATION_WORD}` to finish the project.\n\n**What this does:**\n\t- Deletes the project in discord.\n\t- Adds project to completion board.", color=discord.Color.blue())
                            await ctx.send(embed=embed)
                            msg = await self.bot.wait_for('message', check=check)
                            if msg.content.lower() != CONFIRMATION_WORD: 
                                embed = discord.Embed(title="Confirmation failed!", description="You did not confirm correctly!", color=discord.Color.red())
                                await ctx.send(embed=embed)
                                return
                        guild = ctx.guild
                        category = get(guild.categories, id=projectID)
                        for scan in category.channels:
                            await scan.delete()
                        await category.delete()
                        del data[i]
                        with open(database, "w") as f:
                            json.dump(data, f, indent=2)
                        embed = discord.Embed(title="Project finished!", description="Project removed from active database.\n*Check your DM's for what to do next!*", color=discord.Color.blue())
                        await ctx.send(embed=embed)
                        embed = discord.Embed(title=":confetti_ball: Project complete! :confetti_ball:", description="Congratulations on finishing your project!\n\n**Now what?**\n\t- Upload it to the marketplace.\n\t- Share it with others.\n\t- Get engaged with your audience!", color=discord.Color.blue())
                        await ctx.author.send(embed=embed)
                        return
                i += 1
            embed = discord.Embed(title="Whoops!", description="You need to own a project first.", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.has_role("Verified Developer")
    @commands.command(aliases=["toggle", "toggleinv"])
    async def toggleinvites(self, ctx):
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
    @commands.command(aliases=["description","d"])
    async def desc(self, ctx):
        """Changes the description of your project"""

        ###########################################
        ############## CONFIGURATION ##############
        ###########################################
        # You can change these for your own project
        COMMAND_ENABLED = True
        DATABASE_FILE_NAME = "project-list"
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
            for search in data:
                if search["channelA"] == ctx.channel.id or search["channelB"] == ctx.channel.id:
                    embed = discord.Embed(description=search["description"], color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    return
            embed = discord.Embed(title="Whoops!", description="Command must be executed in a project", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.has_role("Verified Developer")
    @commands.command()
    async def setdesc(self, ctx, *, description: str):
        """Changes the description of your project"""

        ###########################################
        ############## CONFIGURATION ##############
        ###########################################
        # You can change these for your own project
        COMMAND_ENABLED = True
        BLACKLIST_FILTER = True
        BLACKLIST_WORDS = ["example1", "example2"]
        DATABASE_FILE_NAME = "project-list"
        DATABASE_EXTENSION = ".json" # Dont change!
        ###########################################

        if COMMAND_ENABLED is False:
            embed = discord.Embed(title="Command disabled", description="Looks like this command is disabled!", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if BLACKLIST_FILTER and [a for a in BLACKLIST_WORDS if(a in description)]:
            embed = discord.Embed(title="Woah there!", description="Your description contained profanity!\n\n**Reminder:**\n- No descriptions with vulgar names\n- Descriptions must be child friendly", color=discord.Color.red())
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
            def check(m):
                return m.author == ctx.author
            for user in data:
                if user["user_id"] == ctx.author.id:
                    try:
                        projectID = user["project_owned"]
                    except KeyError:
                        pass
                    else:
                        user["description"] = description
                        with open(database, "w") as f:
                            json.dump(data, f, indent=2)
                        embed = discord.Embed(title=f"Success!",
                                            description=f"**Project description is now:** \n{description}",
                                            color=discord.Color.blue())
                        await ctx.send(embed=embed)
                        return
            embed = discord.Embed(title="Whoops!", description="You need to own a project first.", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.has_role("Verified Developer")
    @commands.command()
    async def search(self, ctx):
        """This feature is still in development"""
        guild = ctx.guild
        username = ctx.message.author.name + "'s Projects"
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
                                                                         f"\n**Remember** Set a description before\nstarting an active search with `-desc`"
                                                                         f"\nso people know what the project is!"
                                  , color=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.has_role("Verified Developer")
    @commands.command(aliases=["inv"])
    async def invite(self, ctx, member: discord.Member):
        """Invite people to your project"""

        ###########################################
        ############## CONFIGURATION ##############
        ###########################################
        # You can change these for your own project
        COMMAND_ENABLED = True
        SELF_CHECK = False
        ROLE_CHECK = False
        ALREADY_JOINED_CHECK = False
        ROLE_NAMES = ["Verified Developer", 
                    "Verified Designer", 
                    "Verified Composer", 
                    "Verified Tester"]
        OPT_OUT_LIST_CHECK = True
        DATABASE_OPT_OUT = "opt-out"
        DATABASE_FILE_NAME = "project-list"
        DATABASE_EXTENSION = ".json" # Dont change!
        WRITE_PERMISSION = True
        SERVER_BOT_CHECK = True
        ###########################################
        # When INVITE_SYSTEM is set to false, will
        # automatically add the user to the channel
        # without the user needing to accept
        INVITE_SYSTEM = True 
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
        valid = False
        guild = ctx.guild

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
                    valid = True
                    category = get(guild.categories, id=scan["project_owned"])
                    perms = category.channels
                    use_channel = perms[1]
                    members = scan["members"]
                    description = scan["description"]

        if valid is False:
            embed = discord.Embed(title="Whoops!", description="You need to own a project first.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return 

        if SERVER_BOT_CHECK is True and member.bot is True:
            embed = discord.Embed(title="I'm flattered <3", description="You invited me to your project? *blushes*", color=discord.Color.blue())
            await ctx.send(embed=embed)
            return

        if SELF_CHECK is True and ctx.author == member:
            embed = discord.Embed(title="Uh, *ding dong*, anyone home?", description="You can't invite yourself to your own project", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if ROLE_CHECK is True:
            found = False
            member_roles = member.roles
            member_role_names = []
            for scan in member_roles:
                if scan.name in ROLE_NAMES:
                    found = True
            if found is False:
                embed = discord.Embed(title="Whoops!", description="You can only invite verified roles!", color=discord.Color.red())
                await ctx.send(embed=embed)
                return

        if OPT_OUT_LIST_CHECK is True:
            db = (DATABASE_OPT_OUT+DATABASE_EXTENSION)
            with open(db) as f:
                data = json.load(f)
            for user in data:
                if user["user_id"] == member.id:
                    embed = discord.Embed(title="Whoops!", description="**That member has invites disabled!**\nIf you believe this is a mistake, let them know!", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return

        if ALREADY_JOINED_CHECK is True:
            for scan in use_channel.members:
                if scan.id == member.id:
                    embed = discord.Embed(title="Whoops!", description=f"{member.name} is already in your project!", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    return

        inv_accepted = True

        if INVITE_SYSTEM is True:
            embed = discord.Embed(title="Exciting news!", description=f"**You've been invited!**\nBelow you'll find the project details\n\n**Owner:** {ctx.author.name}\n**Members:** {members}\n**Description:**\n{description}\n\n*You have 1 hour to accept this invite*", color=discord.Color.blue())
            msg = await member.send(embed=embed)  
            await msg.add_reaction('\N{THUMBS UP SIGN}')
            await msg.add_reaction('\N{THUMBS DOWN SIGN}')
            def dmloc(reaction, user):
                return user.id == member.id
            embed = discord.Embed(title="Consider it done!", description=f"**Invite was sent to {member.name} successfully!**\n*They have 1 hour to accept it*", color=discord.Color.blue())
            await ctx.send(embed=embed)
            response, username = await self.bot.wait_for('reaction_add', timeout=3600.0, check=dmloc)
            if response.emoji == '\N{THUMBS UP SIGN}':
                embed = discord.Embed(title=f"{member.name} accepted your invite!", description=f"Go welcome them to your project!", color=discord.Color.blue())
                await ctx.author.send(embed=embed)
                embed = discord.Embed(title=f"{member.name} joined!", color=discord.Color.blue())
                await use_channel.send(embed=embed)
            else:
                embed = discord.Embed(title=f"{member.name} rejected your invite!", description="Talk with users before inviting them!", color=discord.Color.red())
                await ctx.author.send(embed=embed)
                inv_accepted = False
        if inv_accepted is True:
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = WRITE_PERMISSION
            overwrite.read_messages = True
            overwrite.read_message_history = True
            for setperm in perms:
                await setperm.set_permissions(member, overwrite=overwrite)
            if INVITE_SYSTEM is False:
                embed = discord.Embed(title=f"{member.name} was added!", description=f"Welcome to the project {member.mention}!\n\n*Since the invite system is currently disabled,\nyou were automatically added.*", color=discord.Color.blue())
                await use_channel.send(embed=embed)

    @commands.has_role("Verified Developer")
    @commands.command()
    async def leave(self, ctx, project: discord.TextChannel):
        """Invite people to your project"""

        ###########################################
        ############## CONFIGURATION ##############
        ###########################################
        # You can change these for your own project
        COMMAND_ENABLED = True
        CONFIRMATION_WORD = "confirm"
        CONFIRMATION_PROMPT = True
        ###########################################

        if COMMAND_ENABLED is False:
            embed = discord.Embed(title="Command disabled", description="Looks like this command is disabled!",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if "Projects" not in project.category.name:
            return

        def check(m):
            return m.author == ctx.author

        for scan in project.members:
            if scan.id == ctx.author.id:
                if CONFIRMATION_PROMPT is True:
                    embed = discord.Embed(title="Confirm",
                                          description=f"Please type `{CONFIRMATION_WORD}` to leave the project",
                                          color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    msg = await self.bot.wait_for('message', timeout=60.0, check=check)
                    if msg.content.lower() != CONFIRMATION_WORD:
                        embed = discord.Embed(title="Confirmation failed!",
                                              description="You did not confirm correctly!", color=discord.Color.red())
                        await ctx.send(embed=embed)
                        return
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = False
                overwrite.read_messages = False
                overwrite.read_message_history = False
                await project.set_permissions(ctx.author, overwrite=overwrite)
                embed = discord.Embed(title=f"{ctx.author.name} left!", color=discord.Color.red())
                msg = await project.send(embed=embed)
                if ctx.channel.id == project.id:
                    embed = discord.Embed(title="Project left!", description=f"You left the project {project}!",
                                          color=discord.Color.red())
                    msg = await ctx.author.send(embed=embed)
                    return
                else:
                    embed = discord.Embed(title="Project left!", description=f"You left the project {project}!",
                                          color=discord.Color.blue())
                    msg = await ctx.send(embed=embed)
                    return
        embed = discord.Embed(title="Whoops!", description=f"You're not a part of that project",
                              color=discord.Color.red())
        msg = await ctx.send(embed=embed)

    @commands.has_role("Verified Developer")
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason: str):
        """Kick someone from your project"""

        ###########################################
        ############## CONFIGURATION ##############
        ###########################################
        # You can change these for your own project
        COMMAND_ENABLED = True
        SELF_CHECK = True
        VALID_USER_CHECK = True
        SERVER_BOT_CHECK = True
        ADMIN_CHECK = True
        ADMIN_ROLE = "Verified Developer"
        DATABASE_FILE_NAME = "project-list"
        DATABASE_EXTENSION = ".json"
        ###########################################

        try:
            if COMMAND_ENABLED is False:
                embed = discord.Embed(title="Command disabled", description="Looks like this command is disabled!",
                                      color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            if DATABASE_EXTENSION is not ".json":
                embed = discord.Embed(title="WARNING",
                                      description=f"**Invalid database extension set!**\nIt looks like this value was changed.\n\n**Error:** Database must use .json files!\n*Revert this change, and then reload the module.*",
                                      color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            database = (DATABASE_FILE_NAME + DATABASE_EXTENSION)
            valid = False

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
                            category = get(ctx.guild.categories, id=scan["project_owned"])
                            perms = category.channels
                            valid = True

            if valid is False:
                embed = discord.Embed(title="Whoops!", description="Command must be executed in your project!",
                                      color=discord.Color.red())
                msg = await ctx.channel.send(embed=embed)
                return

            if SERVER_BOT_CHECK is True and member.bot is True:
                embed = discord.Embed(title="Wow... ok...", description="I didn't know you felt that way about me :(",
                                      color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            if SELF_CHECK is True and ctx.author == member:
                embed = discord.Embed(title="Uh, *ding dong*, anyone home?",
                                      description="You can't kick yourself from your own project",
                                      color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            if ADMIN_CHECK is True:
                member_roles = member.roles
                member_role_names = []
                for scan in member_roles:
                    if scan.name in ADMIN_ROLE:
                        embed = discord.Embed(title="Whoops!", description="You can't kick Proxima Staff!",
                                              color=discord.Color.red())
                        await ctx.send(embed=embed)
                        return

            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = False
            overwrite.read_messages = False
            overwrite.read_message_history = False
            for scan in category.channels:
                await scan.set_permissions(member, overwrite=overwrite)
            embed = discord.Embed(title=f"{member.name} was kicked!", description=f"**Reason:** {reason}",
                                  color=discord.Color.red())
            msg = await ctx.channel.send(embed=embed)
            embed = discord.Embed(title=f"You were kicked!",
                                  description=f"You got kicked from {ctx.author.name}'s project!\n**Reason:** {reason}",
                                  color=discord.Color.red())
            msg = await member.send(embed=embed)
            return
        except Exception as ex:
            embed = discord.Embed(title="Database Error!",
                                  description=f"**Error:** {ex}",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Developer(bot))
