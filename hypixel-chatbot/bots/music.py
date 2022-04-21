import os
import random
from pathlib import Path
from discord import Embed, File
from discord.ext import commands
from discord.ext.commands.context import Context

from common import SUCCESS_COLOR


class Music(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bot = bot

    @commands.command(name="music")
    async def news(self, ctx: Context):
        file_path = Path("music/" + random.choice(os.listdir("music/")))
        file = File(file_path.absolute())
        embed = Embed(
            title=f"Here is your random music",
            description=file_path.stem,
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)
        await ctx.send(file=file)
