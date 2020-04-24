from constants import BASIC_EMB
from errors import NoUserSpec
from utils import to_column_string


class ProfileCommands:
    async def send_avatar(self, ctx):
        user = ctx.message.mentions[0] if ctx.message.mentions else None
        emb = BASIC_EMB.copy()

        if user is None:
            raise NoUserSpec()

        emb.title = "Avatar of {0}".format(user.display_name)
        emb.set_image(url=user.avatar_url)
        await ctx.send(embed=emb)

    async def send_member_info(self, ctx):
        user = ctx.message.mentions[0] if ctx.message.mentions else None
        emb = BASIC_EMB.copy()

        if user is None:
            raise NoUserSpec()

        emb.title = "Info about {}".format(user.display_name)
        emb.add_field(name="Joined at", value=str(user.joined_at)[:10])
        emb.add_field(name="Status", value=user.status)
        emb.add_field(name="Roles", value=to_column_string(user.roles[::-1]))
        emb.add_field(name="Activity", value=to_column_string(user.activities) if user.activities else "User has no activity right now")

        await ctx.send(embed=emb)
