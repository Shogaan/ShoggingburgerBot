from constants import BASIC_EMB
from db_logic import DatabaseProcessor


class SettingsCommands:
    def __init__(self):
        self.db_proc = DatabaseProcessor()

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

            self.db_proc()._set_greeting(ctx.guild.id, title + "; " + description)

            await ctx.message.delete(delay=3)

            emb = BASIC_EMB.copy()
            emb.title = "Done"
            await ctx.send(embed=emb, delete_after=5)

    async def toggle_greeting_notification(self, ctx):
        """ Turn on or turn off greeting message """

        guild_id = ctx.guild.id

        if self.db_proc.get_enabled_greeting(guild_id):
            is_enabled = False
        else:
            is_enabled = True

        self.db_proc.toggle_enabled_greeting(guild_id, is_enabled)

