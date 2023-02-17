from discord.ext import commands


class APIError(commands.CommandError):
    def __init__(self, server, *args, **kwargs):
        super().__init__(*args, **kwargs)
