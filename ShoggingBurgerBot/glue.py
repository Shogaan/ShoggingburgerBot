import discord

from discord.ext import commands

from chat_logic.chat_commands import ChatCommands
from guild_logic.guild_commands import GuildCommands
from guild_logic.guild_events import GuildEvents
from music_logic.music_main import MusicCommands
from profile_logic.profile_commands import ProfileCommands

from utils import close_database

import asyncio
import os

# --------- Locale ----------



# --------- Locale ----------


# --------- Commands --------

## -------- Profile ---------
class Profile(commands.Cog, name="Profile"):
    @commands.command(help="Return mentioned user's avatar")
    async def avatar(self, ctx):
        await ProfileCommands(ctx).send_avatar()


    @commands.guild_only()
    @commands.command(help="Return information about mentioned member")
    async def member_info(self, ctx):
        await ProfileCommands(ctx).send_member_info()
## -------- Profile ---------

## -------- Guild -----------
class Guild(commands.Cog, name="Server"):
    @commands.guild_only()
    @commands.command(help="Return information about current server")
    async def server_info(self, ctx):
        await GuildCommands(ctx).send_guild_info()

    @commands.guild_only()
    @commands.command(help='-titile- main text\n-Title from several words- Greeting')
    async def set_greeting(self, ctx, *args):
        await GuildCommands(ctx).set_greeting_text(args)
## -------- Guild -----------

## -------- Chat ------------
class Chat(commands.Cog, name="Chat"):
    @commands.command(help="Return link for inviting bot to another server")
    async def get_link(self, ctx):
        await ChatCommands(ctx).send_link()

    @commands.command(help="Sending invite to lamp pub")
    async def to_pub(self, ctx):
        await ChatCommands(ctx).send_invite()

## -------- Chat ------------

## -------- Music -----------
class Music(commands.Cog, name="Music"):
    def __init__(self, bot):
        super().__init__()

        self.music = MusicCommands(bot)

    @commands.guild_only()
    @commands.command()
    async def connect(self, ctx):
        await self.music.connect(ctx)

    @commands.guild_only()
    @commands.command(aliases=['p',])
    async def play(self, ctx, *, args=""):
        await self.music.play(ctx, args)

    @commands.guild_only()
    @commands.command(aliases=['pause', 'resume', 'pr', 'rp',])
    async def pause_resume(self, ctx):
        await self.music.pause_resume(ctx)

    @commands.guild_only()
    @commands.command(aliases=['sk',])
    async def skip(self, ctx):
        await self.music.skip(ctx)

    @commands.guild_only()
    @commands.command(aliases=['volume', 'sv', 'v'])
    async def set_volume(self, ctx, value):
        await self.music.set_volume(ctx, value)

    @commands.guild_only()
    @commands.command(aliases=['disconnect', 'l'])
    async def leave(self, ctx):
        await self.music.disconnect(ctx)
## -------- Music -----------
class System(commands.Cog, name="System"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command(hidden=True)
    async def ping(self, ctx):
        await ctx.send(str(round(self.bot.latency * 10 ** 3)) + "ms")

    @commands.is_owner()
    @commands.command(hidden=True)
    async def shut_down_now(self, ctx):
        close_database()
        await ctx.bot.logout()

    @commands.is_owner()
    @commands.command(hidden=True)
    async def shut_down(self, ctx):
        for guild in ctx.bot.guilds:
            channel = guild.system_channel if guild.system_channel else guild.text_channels[0]
            await channel.send("@everyone! Bot will shut down in 2 minutes!")

        await asyncio.sleep(120)

        close_database()
        await ctx.bot.logout()
# --------- Commands --------

