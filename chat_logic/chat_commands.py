from constants import BASIC_EMB, ERROR_EMB, JOIN_LINK


class ChatCommands:
    def __init__(self, ctx):
        self.ctx = ctx

        self.er_emb = ERROR_EMB

    async def send_link(self):
        await self.ctx.send("https://discordapp.com/oauth2/authorize?client_id=568532677326536704&scope=bot&permissions=8")
