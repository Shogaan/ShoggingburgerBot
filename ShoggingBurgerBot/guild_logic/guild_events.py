from constants import BASIC_EMB, ERROR_EMB, PREFIX

from db_logic import DatabaseProcessor

import sqlite3

class GuildEvents:
    def __init__(self):
        self.er_emb = ERROR_EMB

    async def on_bot_join(self, guild):
        DatabaseProcessor()._create_row_guild_settings(guild.id)

    async def on_bot_leave(self, guild):
        DatabaseProcessor()._remove_row_guild_settings(guild.id)

    async def on_member_join(self, member):
        guild = member.guild
        channel = guild.system_channel if guild.system_channel is not None else guild.text_channels[0]
        text = DatabaseProcessor()._get_greeting(guild.id).split("; ")

        emb = BASIC_EMB.copy()
        emb.title = text[0].format(user=member.display_name, server=guild.name, prefix=PREFIX)
        emb.description = text[1].format(user=member.mention, server=guild.name, prefix=PREFIX)

        await channel.send(embed=emb)

