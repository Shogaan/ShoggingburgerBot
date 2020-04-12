from constants import BASIC_EMB, ERROR_EMB, JOIN_LINK, PUB_LINK


class ChatCommands:
    def __init__(self, ctx):
        self.ctx = ctx

        self.er_emb = ERROR_EMB

    async def send_link(self):
        await self.ctx.send(JOIN_LINK.format(self.ctx.bot.user.id))

    async def send_invite(self):
        emb = BASIC_EMB.copy()
        emb.title = "Welcome, {}!".format(self.ctx.author.display_name)
        emb.description = PUB_LINK

        await self.ctx.send(embed=emb)

