from typing import Dict

import wavelink


class CurrentSong(Dict):
    guild_id: int
    song: wavelink.Track


class LastChannel(Dict):
    guild_id: int
    channel_id: int
