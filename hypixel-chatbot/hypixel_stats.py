from discord.ext import commands
from discord.ext.commands.context import Context


class HypixelStats(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bot = bot

    @commands.group(name="stats")
    async def reminder(self, ctx: Context):
        pass
