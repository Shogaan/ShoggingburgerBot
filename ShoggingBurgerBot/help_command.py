from discord.ext.commands import HelpCommand

from constants import HELP_EMB, PREFIX

from utils import to_column_string


class HelpCommandCustom(HelpCommand):
    def __init__(self):
        super(HelpCommandCustom, self).__init__()

    async def prepare_help_command(self, ctx, command=None):
        emb = HELP_EMB.copy()

        if command is None:
            emb.title = f"Hi, {ctx.message.author.name}! It's a help command. The prefix is '//'"
            cogs = self.get_bot_mapping()
            for cog in cogs:
                if cog == None or cog.qualified_name == "System":
                    continue

                name = cog.qualified_name
                value = to_column_string(cogs[cog])
                emb.add_field(name=name, value=value)

            emb.set_footer(
                    text=f"To see more information ablout command type {PREFIX}help",
                    icon_url="https://i.imgur.com/83bdZJE.jpg")

            await ctx.message.author.send(embed=emb)

    async def send_command_help(self, command):
        emb = HELP_EMB.copy()

        emb.title = command.name
        emb.description = command.help
        if command.aliases:
            value = '\n'.join(command.aliases)
            emb.add_field(name="Aliases", value=value)

        await self.context.send(embed=emb)

