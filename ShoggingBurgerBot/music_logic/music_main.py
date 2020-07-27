import asyncio
import async_timeout
import datetime
import wavelink

from discord.errors import Forbidden
from typing import Union
from wavelink.errors import BuildTrackError

from custom_types import InfoForMusic
from constants import BASIC_EMB, DEFAULT_VOLUME, ERROR_EMB
from constants import URL_TEMPL, YOUTUBE_URL, SOUNDCLOUD_URL
from errors import NotInVoice, NoneTracksFound, IncorrectVolume, StreamsNotPlayable

info_for_music = InfoForMusic()


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
        info_for_music[self.guild_id]["song"] = track

        self.waiting = False

    async def teardown(self):
        try:
            info_for_music.pop(self.guild_id)
            await self.destroy()

        except KeyError:
            pass


class MusicCommands:
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, "wavelink"):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    @staticmethod
    def _get_humanize_time(time: int) -> str:
        time = str(datetime.timedelta(milliseconds=time))
        if len(time) > 7:
            index = time.rfind('.')

        else:
            index = -1

        return time[:-index] if index != -1 else time

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        node = await self.bot.wavelink.initiate_node(host="127.0.0.1",
                                                     port=2333,
                                                     rest_uri='http://127.0.0.1:2333',
                                                     password='youshallnotpass',
                                                     identifier='TEST',
                                                     region='eu_central')

        node.set_hook(self.node_event_hook)

    async def node_event_hook(self, event):
        if isinstance(event, wavelink.TrackEnd):
            try:
                info_for_music[event.player.guild_id]["time"] -= info_for_music[event.player.guild_id]["song"].duration

            except Exception as e:
                self.bot.logger.exception(e)

            await event.player.do_next()

        elif isinstance(event, (wavelink.TrackException, wavelink.TrackStuck)):
            try:
                info_for_music[event.player.guild_id]["time"] -= info_for_music[event.player.guild_id]["song"].duration

            except Exceprtion as e:
                self.bot.logger.exception(e)

            try:
                track = await self.bot.wavelink.build_track(event.track)

            except BuildTrackError:
                emb = ERROR_EMB.copy()
                player = event.player

                channel_id = info_for_music[player.guild_id]["channel"]
                channel = self.bot.get_channel(channel_id)

                emb.title = "**ERROR!** Song couldn't be played!(Streams couldn't be played at all) Skipping..."

                try:
                    await channel.send(embed=emb)

                except Forbidden:
                    await channel.author.send("Error occured! I couldn't send message in channel... So, here it is.",
                                              embed=emb)

                await player.stop()

            else:
                await event.player.play(track)

    async def connect(self, ctx):
        if not ctx.author.voice:
            raise NotInVoice()

        player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                              cls=CustomPlayer)

        info_for_music[ctx.guild.id] = None

        await player.set_volume(DEFAULT_VOLUME)

        await player.connect(ctx.author.voice.channel.id)

    async def disconnect(self, ctx):
        player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                              cls=CustomPlayer)

        try:
            info_for_music.pop(ctx.guild.id)
            await player.destroy()

        except KeyError:
            pass

    async def now_playing(self, ctx):
        player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                              cls=CustomPlayer)

        if not player.is_connected:
            return

        track = player.current

        emb = BASIC_EMB.copy()
        if track is not None:
            emb.title = ":musical_note: Now playing :musical_note:"
            to_end = self._get_humanize_time(track.length - player.position)
            emb.description = "[{}]({})\nTo end {}".format(track.title, track.uri, to_end)

        else:
            emb.title = "Nothing playing"

        await ctx.message.delete()
        await ctx.send(embed=emb, delete_after=5)

    async def play(self, ctx, query):
        player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                              cls=CustomPlayer)

        if not player.is_connected:
            await self.connect(ctx)

        info_for_music[ctx.guild.id]["channel"] = ctx.channel.id

        estimated_time = self._get_humanize_time(
                info_for_music[ctx.guild.id]["time"] - player.position)
        estimated_time = estimated_time if estimated_time != "" else "00:00:00"

        pos_in_queue = player.queue.qsize() + 1  # TODO Make it more properly. When playing - 1, when no - 0

        await ctx.message.delete(delay=2)

        if not URL_TEMPL.match(query):
            if ctx.command.name == "soundcloud":
                query = f"scsearch:{query}"
                platform = "SoundCloud"

            else:
                query = f"ytsearch:{query}"
                platform = "YouTube"

        else:
            if YOUTUBE_URL.match(query):
                platform = "YouTube"

            elif SOUNDCLOUD_URL.match(query):
                platform = "SoundCloud"

            else:
                platform = "some platform"

        tracks = await self.bot.wavelink.get_tracks(f'{query}')

        if not tracks:
            raise NoneTracksFound()

        if isinstance(tracks, wavelink.TrackPlaylist):
            for track in tracks.tracks:
                await player.queue.put(track)
                info_for_music[ctx.guild.id]["time"] += track.duration

            emb = BASIC_EMB.copy()
            emb.title = ":notes: Playlist added :notes:"
            emb.description = "[{}]({})".format(tracks.data["playlistInfo"]["name"],
                                                query if URL_TEMPL.match(query) else None)

            emb.add_field(name="Songs", value=len(tracks.tracks))

        else:
            track = tracks[0]

            if not track.is_stream:
                info_for_music[ctx.guild.id]["time"] += track.duration

            else:
                raise StreamsNotPlayable()

            await player.queue.put(track)

            emb = BASIC_EMB.copy()
            emb.title = ":musical_note: Track added :musical_note:"
            emb.description = "[{}]({})".format(track.title, track.uri)

            emb.add_field(name="Duration",
                          value=self._get_humanize_time(int(track.duration)))

        emb.add_field(name="Position in queue", value=pos_in_queue)

        emb.add_field(name="Estimated time until start", value=estimated_time)

        emb.set_footer(
            text="Requested by {} from {}".format(ctx.author, platform),
            icon_url=ctx.author.avatar_url
        )

        await ctx.send(embed=emb)

        if not player.is_playing:
            await player.do_next()

    async def pause_resume(self, ctx):
        player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                              cls=CustomPlayer)

        if not player.is_connected:
            return

        await ctx.message.delete(delay=2)

        if not player.is_paused:
            emb = BASIC_EMB.copy()
            emb.title = "Pausing..."
            await ctx.send(embed=emb, delete_after=2)
            await player.set_pause(True)

        else:
            emb = BASIC_EMB.copy()
            emb.title = "Starting..."
            await ctx.send(embed=emb, delete_after=2)
            await player.set_pause(False)

    async def skip(self, ctx):
        player = self.bot.wavelink.get_player(guild_id=ctx.guild.id,
                                              cls=CustomPlayer)

        if not player.is_connected:
            return

        await ctx.message.delete(delay=2)

        emb = BASIC_EMB.copy()
        emb.title = "Skipping..."
        await ctx.send(embed=emb, delete_after=2)
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
        await ctx.send(embed=emb, delete_after=2)

        await player.set_volume(value)
