# Developed by Vitzual
# Version 1.0.1
print("###############################")
print("####### Proxima | By Vitzual ########")
print("###############################")

# Integrate required imports
print("Importing packages...")
import traceback
import discord
import asyncio
import math
import random
import sys
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands, tasks
from discord.utils import get
print("Import successful!")

# Sets description, bot prefix, token, and commands
description = '''Proxima Studios bot, by Vitzual'''
bot = commands.Bot(command_prefix='-', description=description)
TOKEN = "HIDDEN" # You can replace this with your own bot token, but remove it before making a commit
startup_extensions = ["Cog.admin", "Cog.developer", "Cog.help", "Cog.math", "Cog.info"]

# Sync with client
print("Syncing with client ID...")
@bot.event
async def on_ready():
    print("Sync successful!")
    print("Running discord branch version",discord.__version__,"(rewrite)")
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
    join_channel = client.get_channel(713248523281498273)
    server_embed = discord.Embed(title=f"{member.display_name} has joined the discord!", description=f"Welcome {member.mention} to Proxima Studios! ", color=discord.Color.blue())
    await client.add_roles(member, role)
    await join_channel.send(embed=server_embed)


# Push bot online
print("Pushing bot online...")
print("Bot is now online, setup complete!\n")
bot.run(TOKEN)