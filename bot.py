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
startup_extensions = ["Cog.admin", "Cog.developer", "Cog.help", "Cog.math", "Cog.info"]

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
    role = get(member.server.roles, name='Community')
    join_channel = client.get_channel(713979112213053442)
    server_embed = discord.Embed(title=f"{member.display_name} has joined the discord!",
                                 description=f"Welcome {member.mention} to Proxima Studios! ",
                                 color=discord.Color.blue())
    await member.add_roles(role)
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

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"{ctx.command} error",
                              description=f"You forgot to all the variables! Check what you need with "
                                          f"`{bot.command_prefix}help {ctx.command.cog_name}`",
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.BotMissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'I need the **{}** permission(s) to run this command.'.format(fmt)
        embed = discord.Embed(title=f"{ctx.command} error",
                              description='I need the **{}** permission(s) to run this command.'.format(fmt),
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.DisabledCommand):
        embed = discord.Embed(title=f"{ctx.command} error",
                              description="This command has been disabled",
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{ctx.command} error",
                              description=f"This command is on cooldown, please try again in "
                                          f"{format(math.ceil(error.retry_after))}s",
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.MissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
        embed = discord.Embed(title=f"{ctx.command} error",
                              description=f"{_message}",
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.NoPrivateMessage):
        try:
            embed = discord.Embed(title=f"{ctx.command} error",
                                  description="This command cannot be sued in direct messages",
                                  color=discord.Color.red())
            embed.set_footer(text=f"{error}")
            await ctx.author.send(embed=embed)
        except discord.Forbidden:
            pass
        return

    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(title=f"{ctx.command} error",
                              description=f"You do not have permission to use this command",
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    # ignore all other exception types, but print them to stderr
    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)

    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


# Push bot online
print("Pushing bot online...")
print("Bot is now online, setup complete!\n")
bot.run(TOKEN)
