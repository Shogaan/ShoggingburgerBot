import asyncio
import async_timeout
import re
import wavelink

from discord.ext import commands
from typing import Union

from errors import NotInVoice, NoneTracksFound, IncorrectVolume
from constants import BASIC_EMB

URL_TEMPL = re.compile('https?:\/\/(?:www\.)?.+')


class CustomPlayer(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.queue = asyncio.Queue()

        self.waiting = False

        # MB add votes

    async def do_next(self):
        if self.is_playing or self.waiting:
            return

        try:
            self.waiting = True
            with async_timeout.timeout(300):
                track = await self.queue.get()

        except asyncio.TimeoutError:
            return await self.teardown()

        await self.play(track)
        self.waiting = False


    async def teardown(self):
        try:
            await self.destroy()

        except KeyError:
            pass


class MusicCommands:
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, "wavelink"):
            self.bot.wavelink = wavelink.Client(self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        node = await self.bot.wavelink.initiate_node(host="127.0.0.1",
                                                     port=2333,
                                                     rest_uri='http://127.0.0.1:2333',
                                                     password='youshallnotpass',
                                                     identifier='TEST',
                                                     region='russia')

        node.set_hook(self.node_event_hook)

    async def node_event_hook(self, event):
        if isinstance(event, (wavelink.TrackStuck, wavelink.TrackException, wavelink.TrackEnd)):
            await event.player.do_next()

    async def connect(self, ctx):
        if not ctx.author.voice:
            raise NotInVoice()

        player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                              cls=CustomPlayer)
        await player.connect(ctx.author.voice.channel.id)

    async def disconnect(self, ctx):
        player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                              cls=CustomPlayer)
        try:
            await player.destroy()
        except KeyError:
            pass

    async def play(self, ctx, query):
        player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                              cls=CustomPlayer)

        if not player.is_connected:
            await self.connect(ctx)

        await ctx.message.delete(delay=2)

        if not URL_TEMPL.match(query):
            query = f"ytsearch:{query}"

        tracks = await self.bot.wavelink.get_tracks(f'{query}')

        if not tracks:
            raise NoneTracksFound()

        if isinstance(tracks, wavelink.TrackPlaylist):
            for track in tracks.tracks:
                await player.queue.put(track)

            emb = BASIC_EMB.copy()
            emb.title = ":notes: Playlist added :notes:"
            emb.description = tracks.data["playlistInfo"]["name"]
            await ctx.send(embed=emb)

        else:
            track = tracks[0]

            await player.queue.put(track)

            emb = BASIC_EMB.copy()
            emb.title = ":notes: Track added :notes:"
            emb.description = track.title
            await ctx.send(embed=emb)

        if not player.is_playing:
            await player.do_next()

    async def pause_resume(self, ctx):
        player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                              cls=CustomPlayer)

        if not player.is_connected:
            return

        await ctx.message.delete(delay=2)

        if player.is_playing:
            emb = BASIC_EMB.copy()
            emb.title = "Pausing..."
            await ctx.send(embed=emb)
            await player.set_pause(True)

        else:
            emb = DASIC_EMB.copy()
            emb.title = "starting..."
            await ctx.send(embed=emb)
            await player.set_pause(False)

    async def skip(self, ctx):
        player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                              cls=CustomPlayer)

        if not player.is_connected:
            return

        await ctx.message.delete(delay=2)

        emb = BASIC_EMB.copy()
        emb.title = "Skipping..."
        await ctx.send(embed=emb)
        await player.stop()

    async def set_volume(self, ctx, value):
        player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                              cls=CustomPlayer)

        value = int(value)

        await ctx.message.delete(delay=2)

        if not 0 < value < 101:
            raise IncorrectVolume()

        emb = BASIC_EMB.copy()
        emb.title = "Volume is {}".format(value)
        await ctx.send(embed=emb)

        await player.set_volume(value)

