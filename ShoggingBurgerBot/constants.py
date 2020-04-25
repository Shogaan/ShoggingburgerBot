from discord import Colour
from discord import Embed
from discord import Activity, ActivityType

from datetime import date

import os
import re

DEBUG = False
END_DAY = date(2020, 6, 30)

TOKEN = os.environ["DISCORD_TOKEN"]
PREFIX = "//"

BASIC_COLOUR = Colour.from_rgb(109, 237, 89)
ERROR_COLOUR = Colour.from_rgb(255, 0, 0)
HELP_COLOUR = Colour.from_rgb(57, 19, 126)

BASIC_EMB = Embed(colour=BASIC_COLOUR)
ERROR_EMB = Embed(colour=ERROR_COLOUR)
HELP_EMB = Embed(colour=HELP_COLOUR)

GREETING_TEMPLATE = "Welcome, {user}!;  We very glad to see you on our awsome server {server}!\nMy prefix is {prefix}."

JOIN_LINK = "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=305294336"

CAFE_LINK = "https://boosty.to/shoggingburger"
CAFE_LINK_INT = "https://www.patreon.com/shoggingburger"
PUB_LINK = "https://discord.gg/5SEM92b"
PUB_ID = 698939991891509258

ACTIVITIES = [
        Activity(type=ActivityType.listening, name="your messages"),
        Activity(type=ActivityType.playing, name="with DNA"),
        Activity(type=ActivityType.watching, name="at awesome loaf"),
        Activity(type=ActivityType.playing, name="Crying for //help")
        ]

DEFAULT_VOLUME = 30

URL_TEMPL = re.compile(r'https?:\/\/(?:www\.)?.+')
YOUTUBE_URL = re.compile(r'https?:\/\/(?:www\.)?.+(youtube|youtu)')
SOUNDCLOUD_URL = re.compile(r'https?:\/\/(?:www\.)?.+soundcloud')

DONATE_LVLS = {
        'Waiter': 1,
        'Barman': 2,
        'Professional barman': 3,
        'Cook': 4,
        'Chief': 5
}
