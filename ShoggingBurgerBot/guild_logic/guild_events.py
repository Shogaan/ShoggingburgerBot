from discord.errors import Forbidden

from constants import BASIC_EMB, PREFIX, PUB_ID

from db_logic import DatabaseProcessor


class GuildEvents:
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

        if guild.id == PUB_ID:
            role = guild.get_role(PUB_ID)
            await member.add_roles(role)

        try:
            await channel.send(embed=emb)
        except Forbidden:
            pass

    async def check_donate_lvl(self, before, after):
        pass
