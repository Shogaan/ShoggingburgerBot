from constants import BASIC_EMB
from db_logic import DatabaseProcessor
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

    async def set_greeting_text(self, ctx, args):
        title = ""
        description = ""
        is_title = True

        for i in args:
            if i.startswith("-") and i.endswith("-") and is_title:
                title += i[1:-1]
                is_title = False

            elif i.startswith('-') and title == "":
                title += i[1:] + " "

            elif i.endswith('-') and description == "":
                title += i[:-1]
                is_title = False

            elif is_title:
                title += i + " "

            elif not is_title:
                description += i + " "

        description = description[:-1]

        DatabaseProcessor()._set_greeting(ctx.guild.id, title + "; " + description)

        await ctx.message.delete(delay=3)

        emb = BASIC_EMB.copy()
        emb.title = "Done"
        await ctx.send(embed=emb, delete_after=5)

