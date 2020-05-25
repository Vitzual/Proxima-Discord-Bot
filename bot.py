import discord
from discord.ext import commands
from discord.utils import get

# Developed by Vitzual
# Version 1.0.1
print("###############################")
print("####### Proxima | By Vitzual ########")
print("###############################")

# Integrate required imports
print("Importing packages...")
print("Import successful!")

# Sets description, bot prefix, token, and commands
description = '''Proxima Studios bot, by Vitzual'''
bot = commands.Bot(command_prefix='-', description=description)
TOKEN = "HIDDEN"  # You can replace this with your own bot token, but remove it before making a commit
startup_extensions = ["Cog.admin", "Cog.developer", "Cog.help", "Cog.math", "Cog.info", "Cog.reload"]

# Sync with client
print("Syncing with client ID...")


@bot.event
async def on_ready():
    print("Sync successful!")
    print("Running discord branch version", discord.__version__, "(rewrite)")


client = discord.Client()

# Load cogs command files
if __name__ == "__main__":  # When script is loaded, this will run
    bot.remove_command("help")
    bot.remove_command("debug")
    bot.remove_command("reload")
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)  # Loads cogs successfully
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))  # Failed to load cog, with error

# Welcome event
@bot.event
async def on_member_join(member):

    ###########################################
    ############## CONFIGURATION ##############
    ###########################################
    WELCOME_MESSAGE = f"{member.display_name} has joined the discord!"
    WELCOME_DESCRIPTION = f"Welcome {member.mention} to Proxima Studios!\n\n**Getting started:**\n- Talk with devs from different projects\n- Get support for numerous projects\n- Join the team! Use `-info` for more info"
    DEFAULT_ROLE = "Community"
    WELCOME_CHANNEL_CATEGORY = "Proxima Overview"
    WELCOME_CHANNEL_NAME = "welcome"
    ###########################################

    await member.add_roles(get(member.guild.roles, name=DEFAULT_ROLE))
    category = get(member.guild.categories, name=WELCOME_CHANNEL_CATEGORY)
    for scan in category.channels:
        if scan.name == WELCOME_CHANNEL_NAME:
            join_channel = scan
    server_embed = discord.Embed(title=WELCOME_MESSAGE,
                                 description=WELCOME_DESCRIPTION,
                                 color=discord.Color.blue())
    await join_channel.send(embed=server_embed)


# Error handling
@bot.event
async def on_command_error(ctx, error):
    # if command has local error handler, return
    if hasattr(ctx.command, 'on_error'):
        return

    # get the original exception
    error = getattr(error, 'original', error)

    if isinstance(error, commands.CommandNotFound):
        return

    # Argument missing error
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Command error",
                              description=f"Oops! Looks like you forgot something.\n**Error:** {error}",
                              color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    # Command cooldown error
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{ctx.command} error",
                              description=f"This command is on cooldown, please try again in "
                                          f"{format(math.ceil(error.retry_after))}s",
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    # Lacking role error
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(title=f"{ctx.command} error",
                              description=f"You do not have permission to use this command",
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return


# Push bot online
print("Pushing bot online...")
print("Bot is now online, setup complete!\n")
bot.run(TOKEN)
