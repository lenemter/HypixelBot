from discord import Embed
from discord.ext import commands
from discord.ext.commands.context import Context


from common import COLOR
from news_utils import get_news


class NewsBot(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bot = bot

    @commands.command(name="news")
    async def news(self, ctx: Context):
        news = get_news(30)
        embed = Embed(
            title=f"Last {len(news)} news",
            description="\n".join((f"[{new.title}]({new.link})" for new in news)),
            color=COLOR,
        )
        await ctx.send(embed=embed)
