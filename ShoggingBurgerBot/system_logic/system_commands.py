from discord.errors import Forbidden

from db_logic import DatabaseProcessor
from utils import parse_command_with_kwargs


class SystemCommands:
    def __init__(self):
        self.db_proc = DatabaseProcessor()

    async def add_don_guild(self, ctx, args):
        kwargs = parse_command_with_kwargs(args)

        unlimit = kwargs.get('unlimit')
        unlimit = unlimit if unlimit is not None else False

        who = 'guild'
        id = kwargs.get('id')
        id = id if id is not None else ctx.guild.id

        unlimit = False

        lvl = None

        self.db_proc.create_row_donators(who, id, unlimit, lvl)

        if unlimit:
            self.db_proc.set_donator_unlimit(id)

    async def add_don_user(self, ctx, args):
        if ctx.message.mentions:
            start = len(ctx.message.mentions)
            args = args[start:]

        kwargs = parse_command_with_kwargs(args)

        unlimit = kwargs.get('unlimit')
        unlimit = unlimit if unlimit is not None else date.today() <= END_DAY

        who = 'member'
        id = kwargs.get('id')
        id = id if id is not None else ctx.message.mentions[0].id

        lvl = kwargs.get('lvl')
        lvl = lvl if lvl is not None else 1

        self.db_proc.create_row_donators(who, id, lvl)

        if unlimit:
            self.db_proc.set_donator_unlimit(id)

    async def set_don_unlimit(self, ctx, args):
        if ctx.message.mentions:
            id = ctx.message.mentions[0].id

        else:
            id = int(args[0])

        self.db_proc.set_donator_unlimit(id)

    async def unset_don_unlimit(ctx, args):
        if ctx.message.mentions:
            id = ctx.message.mentions[0].id

        else:
            id = int(args[0])

        self.db_proc.unset_donator_unlimit(id)

    async def remove_don_guild(ctx, args):
        id = int(args[0]) if args else ctx.guild.id

        self.db_proc.remove_row_donators(id)

    async def remove_don_user(ctx, args):
        if ctx.message.mentions:
            id = ctx.message.mentions[0].id

        else:
            id = int(args[0])

        self.db_proc.remove_row_donators(id)

    async def send_message(self, ctx, message):
        message_to_send = "@everyone " + message

        for guild in ctx.bot.guilds:
            channel = guild.system_channel if guild.system_channel is not None else guild.     text_channels[0]

            try:
                await channel.send(message_to_send)

            except Forbidden:
                pass

