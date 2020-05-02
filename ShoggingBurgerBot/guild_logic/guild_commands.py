from constants import BASIC_EMB
from utils import to_column_string


class GuildCommands:
    async def send_guild_info(self, ctx):
        guild = ctx.guild

        emb = BASIC_EMB.copy()

        emb.title = guild.name

        emb.add_field(name="Region", value=str(guild.region).title())
        emb.add_field(name="Members", value=guild.member_count)
        emb.add_field(name="Owner", value=guild.owner.display_name)
        emb.add_field(name="Roles", value=to_column_string(guild.roles))
        emb.add_field(name="Text channels", value=to_column_string(guild.text_channels))
        emb.add_field(name="Voice channels", value=to_column_string(guild.voice_channels))

        await ctx.message.delete(delay=2)

        await ctx.send(embed=emb)

