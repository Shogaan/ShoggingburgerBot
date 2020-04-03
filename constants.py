from discord import Colour
from discord import Embed

import os

TOKEN = os.environ["DISCORD_TOKEN"]
PREFIX = "//"

BASIC_COLOUR = Colour.from_rgb(109, 237, 89)
ERROR_COLOUR = Colour.from_rgb(255, 0, 0)
HELP_COLOUR = Colour.from_rgb(57, 19, 126)

BASIC_EMB = Embed(colour=BASIC_COLOUR)
ERROR_EMB = Embed(colour=ERROR_COLOUR)
HELP_EMB = Embed(colour=HELP_COLOUR)

GREETING_TEMPLATE = "Welcome, {user}!;  We very glad to see you on our awsome server {server}!\nMy prefix is {prefix}."

JOIN_LINK = "https://discordapp.com/oauth2/authorize?client_id=568532677326536704&scope=bot&permissions=8"
