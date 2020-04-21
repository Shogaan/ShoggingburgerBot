import discord

from discord.ext import commands

from chat_logic.chat_commands import ChatCommands
from guild_logic.guild_commands import GuildCommands
from guild_logic.guild_events import GuildEvents
from music_logic.music_main import MusicCommands
from profile_logic.profile_commands import ProfileCommands

from constants import PREFIX
from utils import close_database

import asyncio
import os

# --------- Commands --------

## -------- Profile ---------
class Profile(commands.Cog, name="Profile"):
    @commands.command(aliases=['av', 'ava',],
                      help="Return mentioned user's avatar")
    async def avatar(self, ctx):
        await ProfileCommands(ctx).send_avatar()

    @commands.guild_only()
    @commands.command(aliases=['mi', 'memberinfo', 'meminfo', 'mem_info'],
                      help="Return information about mentioned member")
    async def member_info(self, ctx):
        await ProfileCommands(ctx).send_member_info()
## -------- Profile ---------

## -------- Guild -----------
class Guild(commands.Cog, name="Server"):
    @commands.guild_only()
    @commands.command(aliases=['serverinfo', 'guild_info', 'guildinfo', 'si', 'gi'],
                      help="Return information about current server")
    async def server_info(self, ctx):
        await GuildCommands(ctx).send_guild_info()

    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['setgreeting', 'setgreet', 'set_greet', 'sg'],
                      help='To set new greeting type:\n`{prefix}set_greeting -titile- main text`\nor\n'
                           '`{prefix}set_greeting -Title from several words- Greeting`'
                           '\nIn every part of your greeting you can type:'
                           '```{{user}} - to refer to user\n'
                           '{{server}} - to display server\'s name\n'
                           '{{prefix}} - to display my prefix```\n'
                           '**You need to be an administrator!**'.format(prefix=PREFIX))
    async def set_greeting(self, ctx, *args):
        await GuildCommands(ctx).set_greeting_text(args)
## -------- Guild -----------

## -------- Chat ------------
class Chat(commands.Cog, name="Chat"):
    @commands.command(aliases=['getlink', 'gl'],
                      help="Return link for inviting bot to another server")
    async def get_link(self, ctx):
        await ChatCommands(ctx).send_link()

    @commands.command(aliases=['randomcat', 'rand_cat', 'randcat', 'rc'],
                      help="Return cute kitty")
    async def random_cat(self, ctx):
        await ChatCommands(ctx).send_random_cat()

    @commands.command(aliases=['tp'],
                      help="Sending invite to lamp pub")
    async def to_pub(self, ctx):
        await ChatCommands(ctx).send_invite()

## -------- Chat ------------

## -------- Music -----------
class Music(commands.Cog, name="Music"):
    def __init__(self, bot):
        super().__init__()

        self.music = MusicCommands(bot)

    @commands.guild_only()
    @commands.command(aliases=['con'],
                      help="Connect me to channel")
    async def connect(self, ctx):
        await self.music.connect(ctx)

    @commands.guild_only()
    @commands.command(aliases=['np', 'nowplaying',],
                      help="Return information about playing song")
    async def now_playing(self, ctx):
        await self.music.now_playing(ctx)

    @commands.guild_only()
    @commands.command(aliases=['p',],
                      help="Play your awesome music from given `URL` or search it in YouTube")
    async def play(self, ctx, *, args=""):
        await self.music.play(ctx, args)

    @commands.guild_only()
    @commands.command(name="soundcloud",
                      aliases=['sc',],
                      help="Same as `play` but search in SoundCloud")
    async def sc(self, ctx, *, args=""):
        await self.music.play(ctx, args)

    @commands.guild_only()
    @commands.command(aliases=['pause', 'resume', 'pr', 'rp',],
                      help="Starts or pausing music")
    async def pause_resume(self, ctx):
        await self.music.pause_resume(ctx)

    @commands.guild_only()
    @commands.command(aliases=['sk',],
                      help="Skip playing song")
    async def skip(self, ctx):
        await self.music.skip(ctx)

    @commands.guild_only()
    @commands.command(aliases=['volume', 'sv', 'v'],
                      help="Set volume of player")
    async def set_volume(self, ctx, value):
        await self.music.set_volume(ctx, value)

    @commands.guild_only()
    @commands.command(aliases=['disconnect', 'l'],
                      help="Disconnect me from channel")
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
        exit(0)

    @commands.is_owner()
    @commands.command(hidden=True)
    async def shut_down(self, ctx):
        for guild in ctx.bot.guilds:
            channel = guild.system_channel if guild.system_channel else guild.text_channels[0]
            await channel.send("@everyone! Bot will shut down in 2 minutes!",
                                delete_after=150)

        await asyncio.sleep(120)

        close_database()
        exit(0)
# --------- Commands --------

