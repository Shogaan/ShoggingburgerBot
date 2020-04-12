from discord.ext.commands import HelpCommand

from constants import HELP_EMB

from utils import to_column_string


class HelpCommandCustom(HelpCommand):
    def __init__(self):
        super(HelpCommandCustom, self).__init__()

    async def prepare_help_command(self, ctx, command=None):
        emb = HELP_EMB.copy()

        if command is None:
            emb.title = f"Hi, {ctx.message.author.name}! It's a help command. The prefix is '//'"
            # emb.add_field(name="Profile", value="avatar `@mention`\nmember_info `@mention`")
            # get_bot_mapping
            cogs = self.get_bot_mapping()
            for cog in cogs:
                if cog == None or cog.qualified_name == "System":
                    continue

                name = cog.qualified_name
                value = to_column_string(cogs[cog])
                emb.add_field(name=name, value=value)

            await ctx.message.author.send(embed=emb)

    async def send_command_help(self, command):
        emb = HELP_EMB.copy()

        emb.title = command.name
        emb.description = command.help
        value = '\n'.join(command.aliases)
        emb.add_field(name="Aliases", value=value)
        await self.context.send(embed=emb)
