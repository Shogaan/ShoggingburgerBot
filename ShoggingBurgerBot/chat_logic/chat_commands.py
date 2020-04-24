import json
import requests

from constants import BASIC_EMB, JOIN_LINK, PUB_LINK


class ChatCommands:
    async def send_invite(self, ctx):
        emb = BASIC_EMB.copy()
        emb.title = "Welcome, {}!".format(ctx.author.display_name)
        emb.url = PUB_LINK

        await ctx.message.delete(delay=2)

        await ctx.send(embed=emb)

    async def send_link(self, ctx):
        await ctx.message.delete(delay=2)

        await ctx.send(JOIN_LINK.format(ctx.bot.user.id))

    async def send_random_cat(self, ctx):
        req = requests.get(url="http://aws.random.cat//meow")

        emb = BASIC_EMB.copy()
        emb.title = ":smiley_cat: Here's your cat :smiley_cat:"
        emb.set_image(url=req.json()['file'])

        await ctx.send(embed=emb)

