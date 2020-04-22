from constants import BASIC_EMB, PREFIX

from db_logic import DatabaseProcessor


class GuildEvents:
    async def on_bot_join(self, guild):
        DatabaseProcessor()._create_row_guild_settings(guild.id)

    async def on_bot_leave(self, guild):
        DatabaseProcessor()._remove_row_guild_settings(guild.id)

    async def on_member_join(self, member, bot):
        guild = member.guild
        channel = guild.system_channel if guild.system_channel is not None else guild.text_channels[0]
        if channel.permissions_for(bot).send_messages:
            text = DatabaseProcessor()._get_greeting(guild.id).split("; ")

            emb = BASIC_EMB.copy()
            emb.title = text[0].format(user=member.display_name, server=guild.name, prefix=PREFIX)
            emb.description = text[1].format(user=member.mention, server=guild.name, prefix=PREFIX)

            if guild.id == 698939991891509258:
                role = guild.get_role(698976288010010714)
                await member.add_roles(role)

            await channel.send(embed=emb)

