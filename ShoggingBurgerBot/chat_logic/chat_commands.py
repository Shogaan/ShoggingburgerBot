from constants import BASIC_EMB, ERROR_EMB, JOIN_LINK


class ChatCommands:
    def __init__(self, ctx):
        self.ctx = ctx

        self.er_emb = ERROR_EMB

    async def send_link(self):
        await self.ctx.send(JOIN_LINK.format(self.ctx.bot.user.id))

