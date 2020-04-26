from aiohttp.client_exceptions import ClientConnectionError
from discord.errors import Forbidden

from constants import BASIC_EMB, PREFIX, PUB_ID
from constants import DONATE_LVLS, END_DAY

from db_logic import DatabaseProcessor

from datetime import date


class GuildEvents:
    def __init__(self):
        self.db_proc = DatabaseProcessor()

    async def on_bot_join(self, guild):
        self.db_proc._create_row_guild_settings(guild.id)

    async def on_bot_leave(self, guild):
        self.db_proc._remove_row_guild_settings(guild.id)

    async def on_member_join(self, member):
        guild = member.guild
        channel = guild.system_channel if guild.system_channel is not None else guild.text_channels[0]
        text = self.db_proc._get_greeting(guild.id).split("; ")

        emb = BASIC_EMB.copy()
        emb.title = text[0].format(user=member.display_name, server=guild.name, prefix=PREFIX)
        emb.description = text[1].format(user=member.mention, server=guild.name, prefix=PREFIX)

        if guild.id == PUB_ID:
            role = guild.get_role(PUB_ID)
            await member.add_roles(role)

        try:
            await channel.send(embed=emb)
        except (Forbidden, ClientConnectionError):
            pass

    async def check_donate_lvl(self, before, after):
        if before.top_role < after.top_role:
            id = after.id
            role = after.top_role.name
            if role not in DONATE_LVLS.keys():
                return

            lvl = DONATE_LVLS[role]

            if not self.db_proc.is_donator(id):
                who = 'member'
                unlimit = date.today() <= END_DAY
                self.db_proc.create_row_donators(who, id, unlimit, lvl)

            else:
                self.db_proc.update_donator_lvl(id, lvl)

        elif before.top_role > after.top_role:
            id = after.id
            role = after.top_role.name

            if self.db_proc.is_donator(id):
                if self.db_proc.is_unlimit(id):
                    role = before.top_role
                    await after.add_roles(role)

                else:
                    if role not in DONATE_LVLS.keys():
                        self.db_proc.remove_row_donators(id)

                    else:
                        lvl = DONATE_LVLS[role]
                        self.db_proc.update_donator_lvl(id, lvl)
