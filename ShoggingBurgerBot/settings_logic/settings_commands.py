from constants import BASIC_EMB
from db_logic import DatabaseProcessor


class SettingsCommands:
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

