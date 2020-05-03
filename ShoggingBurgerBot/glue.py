import discord

from discord.ext import commands
from discord.errors import Forbidden

from chat_logic.chat_commands import ChatCommands
from donate_commands import DonateCommands
from guild_logic.guild_commands import GuildCommands
from music_logic.music_main import MusicCommands
from profile_logic.profile_commands import ProfileCommands
from settings_logic.settings_commands import SettingsCommands
from system_logic.system_commands import SystemCommands

from constants import PREFIX
from constants import DEBUG, END_DAY
from errors import NotDonator
from db_logic import DatabaseProcessor
from utils import close_database, parse_command_with_kwargs

from datetime import date

import asyncio
import os

# --------- Checks ----------

def is_donator_or_owner():
    async def predicate(ctx):
        is_donator_guild = ctx.guild.id in DatabaseProcessor().get_donators_guilds()
        is_donator_member = ctx.author.id in DatabaseProcessor().get_donators_members()

        if (is_donator_guild or
            is_donator_member or
            date.today() <= END_DAY or
            DEBUG or
            await ctx.bot.is_owner(ctx.author)):

            return True

        else:
            raise NotDonator()

    return commands.check(predicate)

# --------- Checks ----------

# --------- Commands --------

## -------- Chat ------------
class Chat(commands.Cog, name="Chat"):
    def __init__(self):
        super().__init__()

        self.chat = ChatCommands()

    @commands.command(aliases=['getlink', 'gl'],
                      help="Return link for inviting bot to another server")
    async def get_link(self, ctx):
        await self.chat.send_link(ctx)

    @commands.command(aliases=['randomcat', 'rand_cat', 'randcat', 'rc'],
                      help="Return cute kitty")
    async def random_cat(self, ctx):
        await self.chat.send_random_cat(ctx)

    @commands.command(aliases=['tp'],
                      help="Sending invite to lamp pub")
    async def to_pub(self, ctx):
        await self.chat.send_invite(ctx)

## -------- Chat ------------

## -------- Donate ----------
class Donate(commands.Cog, name="Donate"):
    def __init__(self):
        super().__init__()

        self.donate_class = DonateCommands()

    @commands.command(help="Send links for donation")
    async def donate(self, ctx):
        await self.donate_class.send_donate_link(ctx)

    @commands.guild_only()
    @commands.command(hidden=True)
    async def guild_donate_status(self, ctx):
        await ctx.send("In the development")

    @commands.command(hidden=True)
    async def user_donate_status(self, ctx):
        await ctx.send("In the development")
## -------- Donate ----------

## -------- Guild -----------
class Guild(commands.Cog, name="Server"):
    def __init__(self):
        super().__init__()

        self.guild = GuildCommands()

    @commands.guild_only()
    @commands.command(aliases=['serverinfo', 'guild_info', 'guildinfo', 'si', 'gi'],
                      help="Return information about current server")
    async def server_info(self, ctx):
        await self.guild.send_guild_info(ctx)
## -------- Guild -----------

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
    @commands.command(aliases=['sk', 's'],
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

## -------- Profile ---------
class Profile(commands.Cog, name="Profile"):
    def __init__(self):
        super().__init__()

        self.profile = ProfileCommands()

    @commands.command(aliases=['av', 'ava',],
                      help="Return mentioned user's avatar")
    async def avatar(self, ctx):
        await self.profile.send_avatar(ctx)

    @commands.guild_only()
    @commands.command(aliases=['mi', 'memberinfo', 'meminfo', 'mem_info'],
                      help="Return information about mentioned member")
    async def member_info(self, ctx):
        await self.profile.send_member_info(ctx)
## -------- Profile ---------

## -------- Settings --------
class Settings(commands.Cog, name="Settings"):
    def __init__(self):
        super().__init__()

        self.settings = SettingsCommands()

    @is_donator_or_owner()
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
        await self.settings.set_greeting_text(ctx, args)


## -------- Settings --------

class System(commands.Cog, name="System"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.db_proc = DatabaseProcessor()

        self.system = SystemCommands()

    @commands.is_owner()
    @commands.command(hidden=True)
    async def add_donator_guild(self, ctx, *args):
        await self.system.add_don_guild(ctx, args)

    @commands.is_owner()
    @commands.command(hidden=True)
    async def add_donator_user(self, ctx, *args):
        await self.system.add_don_user(ctx, args)

    @commands.is_owner()
    @commands.command(hidden=True)
    async def set_donator_unlimit(self, ctx, *args):
        await self,system.set_don_unlimit(ctx, args)

    @commands.is_owner()
    @commands.command(hidden=True)
    async def unset_donator_unlimit(self, ctx, *args):
        await self.system.unset_don_unlimit(ctx, args)

    @commands.is_owner()
    @commands.command(hidden=True)
    async def remove_donator_guild(self, ctx, *args):
        await self.system.remove_don_guild(ctx, args)

    @commands.is_owner()
    @commands.command(hidden=True)
    async def remove_donator_user(self, ctx, *args):
        await self.system.remove_don_user(ctx, args)

    @commands.command(hidden=False)
    async def ping(self, ctx):
        await ctx.send(str(round(self.bot.latency * 10 ** 3)) + "ms")

    @commands.is_owner()
    @commands.command(hidden=True)
    async def send_message(self, ctx, *, message):
        await self.system.send_message(ctx, message)

    @commands.is_owner()
    @commands.command(hidden=True)
    async def shut_down_now(self, ctx):
        close_database()
        await ctx.bot.shut_down()

    @commands.is_owner()
    @commands.command(hidden=True)
    async def shut_down(self, ctx):
        for guild in ctx.bot.guilds:
            channel = guild.system_channel if guild.system_channel else guild.text_channels[0]

            try:
                await channel.send("@everyone! Bot will shut down in 2 minutes!",
                                delete_after=119)

            except Forbidden:
                continue

        await asyncio.sleep(120)

        close_database()
        await ctx.bot.shut_down()
# --------- Commands --------
