from typing import Dict


class InfoForMusic(Dict):
    def __init__(self, *args, **kwargs):
        super().__init__()

    def __setitem__(self, key, value):
        if value is None:
            value = {
                "song": None,
                "channel": None,
                "time": 0
            }
        super().__setitem__(key, value)
