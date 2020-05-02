import aiohttp
import json

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
        async with aiohttp.ClientSession() as session:
            async with session.get("http://aws.random.cat//meow") as resp:
                json_resp = await resp.json()
                cat_file_url = json_resp['file']

                del json_resp

        emb = BASIC_EMB.copy()
        emb.title = ":smiley_cat: Here's your cat :smiley_cat:"
        emb.set_image(url=cat_file_url)

        await ctx.send(embed=emb)

