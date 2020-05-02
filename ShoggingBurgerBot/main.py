from discord import Activity, ActivityType
from discord.ext import commands
from discord.errors import Forbidden

from websockets.exceptions import ConnectionClosedError

import asyncio
import sys

from guild_logic.guild_events import GuildEvents
from topgg_logic.topgg_main import TopGG
from glue import Chat, Donate, Guild, Music, Profile, Settings, System

from help_command import HelpCommandCustom

from db_logic import DatabaseProcessor
from constants import ACTIVITIES
from constants import ERROR_EMB
from constants import TOKEN, PREFIX
from constants import PUB_ID
from constants import DEBUG
from utils import close_database


class Bot(commands.Bot):
    def __init__(self):
        super(Bot, self).__init__(command_prefix=PREFIX, help_command=HelpCommandCustom())
        self.activity = Activity(name="Starting", type=ActivityType.playing)

        self.guild_events = GuildEvents()

        self.add_cog(Chat())
        self.add_cog(Donate())
        self.add_cog(Music(self))
        self.add_cog(Profile())
        self.add_cog(Guild())  # Because in help command it is "Server" 
        self.add_cog(Settings())
        self.add_cog(System(self))

        if not DEBUG:
            self.add_cog(TopGG(self))

    async def on_ready(self):
        db_p = DatabaseProcessor()

        guilds = [i.id for i in self.guilds]
        wr_guilds = [i[0] for i in db_p._get_guilds()]

        for guild in guilds:
            if not guild in wr_guilds:
                db_p._create_row_guild_settings(guild)

        wr_guilds = [i[0] for i in db_p._get_guilds()]

        for guild in wr_guilds:
            if guild not in guilds:
                db_p._remove_row_guild_settings(guild)

        self.loop.create_task(self.dynamic_activity())

        print("Bot on-line")

    async def on_resume(self):
        print("Shutting down...")
        close_database()
        print("Done")
        exit(0)

    async def on_command_error(self, ctx, err):
        emb = ERROR_EMB.copy()

        err = str(err) if str(err)[-1] != '.' else str(err)[:-1]

        emb.title = "**ERROR!** " + err + "!"

        try:
            await ctx.send(embed=emb)

        except Forbidden:
            await ctx.author.send("Error occured! I can not send message in channel... So, here it is.",
                                  embed=emb)

    async def dynamic_activity(self):
        await self.wait_until_ready()

        while True:
            for activity in ACTIVITIES:
                try:
                    await self.change_presence(activity=activity)

                except ConnectionClosedError:
                    pass

                await asyncio.sleep(240)

    async def shut_down(self):
        if not DEBUG:
            await self.cogs['TopGG'].dblpy.close()

        exit(0)

    # ------- Guilds ----------
    async def on_guild_join(self, guild):
        await self.guild_events.on_bot_join(guild)

    async def on_guild_remove(self, guild):
        await self.guild_events.on_bot_leave(guild)

    async def on_member_join(self, member):
        await self.guild_events.on_member_join(member)

    async def on_member_update(self, before, after):
        if not before.bot and (before.guild.id == PUB_ID or DEBUG):
            await self.guild_events.check_donate_lvl(before, after)
    # ------- Guilds ----------


if __name__ == "__main__":
    DEBUG = True if len(sys.argv) > 1 and sys.argv[1] == '-d' else False

    Bot().run(TOKEN)
