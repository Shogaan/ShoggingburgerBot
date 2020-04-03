from constants import BASIC_EMB, ERROR_EMB
from utils import to_column_string

class ProfileCommands:
    def __init__(self, ctx):
        self.ctx = ctx

        self.er_emb = ERROR_EMB

    async def send_avatar(self):
        user = self.ctx.message.mentions[0] if self.ctx.message.mentions else None
        emb = BASIC_EMB.copy()

        if user is None:
            self.er_emb.title = "**ERROR!** At least one user must be specified!"
            await self.ctx.send(embed=self.er_emb)
            return

        emb.title = "Avatar of {0}".format(user.display_name)
        emb.set_image(url=user.avatar_url)
        await self.ctx.send(embed=emb)

    async def send_member_info(self):
        if not self.ctx.guild:
            self.er_emb.title = "**ERROR!** This command works **only** on server!"

            await self.ctx.send(embed=self.er_emb)
            return

        user = self.ctx.message.mentions[0] if self.ctx.message.mentions else None
        emb = BASIC_EMB.copy()

        if user is None:
            self.er_emb.title = "**ERROR!** At least one user must be specified!"

            await self.ctx.send(embed=self.er_emb)
            return

        emb.title = "Info about {}".format(user.display_name)
        emb.add_field(name="Joined at", value=str(user.joined_at)[:10])
        emb.add_field(name="Status", value=user.status)
        emb.add_field(name="Roles", value=to_column_string(user.roles[::-1]))
        emb.add_field(name="Activity", value=to_column_string(user.activities) if user.activities else "User has no activity right now")

        await self.ctx.send(embed=emb)

