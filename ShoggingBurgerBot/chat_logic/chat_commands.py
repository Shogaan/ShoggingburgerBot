import json
import requests

from constants import BASIC_EMB, JOIN_LINK, PUB_LINK


class ChatCommands:
    def __init__(self, ctx):
        self.ctx = ctx

    async def send_invite(self):
        emb = BASIC_EMB.copy()
        emb.title = "Welcome, {}!".format(self.ctx.author.display_name)
        emb.url = PUB_LINK

        await self.ctx.message.delete(delay=2)

        await self.ctx.send(embed=emb)

    async def send_link(self):
        await self.ctx.message.delete(delay=2)

        await self.ctx.send(JOIN_LINK.format(self.ctx.bot.user.id))

    async def send_random_cat(self):
        req = requests.get(url="http://aws.random.cat//meow")

        emb = BASIC_EMB.copy()
        emb.title = ":smiley_cat: Here's your cat :smiley_cat:"
        emb.set_image(url=req.json()['file'])

        await self.ctx.send(embed=emb)

