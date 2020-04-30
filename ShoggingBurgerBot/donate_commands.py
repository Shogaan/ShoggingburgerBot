from discord.errors import Forbidden

from constants import BASIC_EMB, DONATE_LINKS


class DonateCommands:
    async def send_donate_link(self, ctx):
        emb = BASIC_EMB.copy()

        emb.title = "Your links"
        emb.description = "[Boosty]({}) or [Patreon]({})\n" \
                          "Donate features while available **only** on Boosty! " \
                          "In other case go to pub and ask there the administrator".format(*DONATE_LINKS)

        try:
            await ctx.send(embed=emb)

        except Forbidden:
            await ctx.author.send("I couldn't send the mesaage to channel", embed=emb)

