from dbl import DBLClient

from discord.ext import commands

from constants import TOPGG_TOKEN

from datetime import datetime


class TopGG(commands.Cog, name="System"):
    def __init__(self, bot):
        self.bot = bot

        self.dblpy = DBLClient(bot=self.bot,
                               token=TOPGG_TOKEN,
                               autopost=True)

    async def on_guild_post(self):
        print(str(datetime.today()) + " --- Posted on {} guilds".format(self.dblpy.guild_count()))
