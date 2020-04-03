import discord

from discord.ext import commands

from chat_logic.chat_commands import ChatCommands
from guild_logic.guild_commands import GuildCommands
from guild_logic.guild_events import GuildEvents
from music_logic.music_main import MusicCommands
from profile_logic.profile_commands import ProfileCommands
from help_command import HelpCommandCustom

from constants import TOKEN, PREFIX
from utils import close_database

import os

bot = commands.Bot(command_prefix=PREFIX, help_command=HelpCommandCustom())

# --------- Locale ----------



# --------- Locale ----------


# --------- Commands --------

## -------- Profile ---------
@bot.command(help="Return mentioned user's avatar")
async def avatar(ctx):
    await ProfileCommands(ctx).send_avatar()


@bot.command(help="Return information about mentioned member")
async def member_info(ctx):
    await ProfileCommands(ctx).send_member_info()
## -------- Profile ---------

## -------- Guild -----------
@bot.command(help="Return information about current server")
async def server_info(ctx):
    await GuildCommands(ctx).send_guild_info()

@bot.command(help='-titile- main text\n-Title from several words- Greeting')
async def set_greeting(ctx, *args):
    await GuildCommands(ctx).set_greeting_text(args)

@bot.command(help="Enter new prefix. Max length is 10 symbols")
async def set_prefix(ctx, *new_prefix):
    await GuildCommands(ctx).set_prefix(new_prefix)
## -------- Guild -----------

## -------- Chat ------------
@bot.command(help="Return link for inviting bot to another server")
async def get_link(ctx):
    await ChatCommands(ctx).send_link()

## -------- Chat ------------

## -------- Music -----------
# TODO: Later automate this
@bot.command()
async def connect(ctx):
    await MusicCommands(ctx).connect()

@bot.command()
async def leave(ctx):
    await MusicCommands(ctx).disconnect()
## -------- Music -----------

@bot.command(hidden=True)
async def ping(ctx):
    await ctx.send(str(round(bot.latency * 10 ** 3)) + "ms")

# --------- Commands --------


# --------- Events ----------

@bot.event
async def on_ready():
    print("Bot on-line")

@bot.event
async def on_disconnect():
    print("\nShutting down...")
    close_database()
    print("Done")
    exit(0)

@bot.event
async def on_resumed():
    print("\nShutting down...")
    close_database()
    print("Done")
    exit(0)

## -------- Guild -----------
@bot.event
async def on_guild_join(guild):
    await GuildEvents().on_bot_join(guild)

@bot.event
async def on_guild_remove(guild):
    await GuildEvents().on_bot_leave(guild)

@bot.event
async def on_member_join(member):
    await GuildEvents().on_member_join(member)

## -------- Guild -----------

# --------- Events ----------

bot.run(TOKEN)

