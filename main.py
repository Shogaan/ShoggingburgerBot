from discord.ext import commands

from guild_logic.guild_events import GuildEvents
from glue import Profile, Guild, Chat, Music, System

from help_command import HelpCommandCustom

from db_logic import DatabaseProcessor
from constants import TOKEN, PREFIX
from utils import close_database

class Bot(commands.Bot):
    def __init__(self):
        super(Bot, self).__init__(command_prefix=PREFIX, help_command=HelpCommandCustom())

        self.guild_events = GuildEvents()

        self.add_cog(Profile())
        self.add_cog(Guild())
        self.add_cog(Chat())
        self.add_cog(Music(self))
        self.add_cog(System(self))

    async def on_ready(self):
        db_p = DatabaseProcessor()

        guilds = [i.id for i in self.guilds]
        wr_guilds = [i[0] for i in db_p._get_guilds()]

        for guild in guilds:
            if not guild in wr_guilds:
                db_p._create_row_guild_settings(guild)

        wr_guilds = [i[0] for i in db_p._get_guilds()]

        for guild in wr_guilds:
            if not guild in guilds:
                db_p._remove_row_guild_settings(guild)

        print("Bot on-line")

    async def on_disconnect(self):
        print("Shutting down...")
        close_database()
        print("Done")
        exit(0)

    async def on_resume(self):
        print("Shutting down...")
        close_database()
        print("Done")
        exit(0)

    # ------- Guilds ----------
    async def on_guild_join(self, guild):
        await self.guild_events.on_bot_join(guild)

    async def on_guild_remove(self, guild):
        await self.guild_events.on_bot_leave(guild)

    async def on_member_join(self, member):
        await self.guild_events.on_mamber_join(member)
    # ------- Guilds ----------


Bot().run(TOKEN)

