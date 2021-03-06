from discord.ext.commands import CommandError


class NoUserSpec(CommandError):
    def __str__(self):
        return "At least one user must be specified"


class NotInVoice(CommandError):
    def __str__(self):
        return "You must be in voice channel"


class NotDonator(CommandError):
    def __str__(self):
        return "You need to be a donator"


class NoneTracksFound(CommandError):
    def __str__(self):
        return "Zero tracks found, try again or change query"


class IncorrectVolume(CommandError):
    def __str__(self):
        return "Minimum volume is 1, maximum - 100"


class StreamsNotPlayable(CommandError):
    def __str__(self):
        return "Streams couldn't be played"
