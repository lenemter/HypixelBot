from common import (
    COMMAND_PREFIX,
    ERROR_COLOR,
    REGULAR_COLOR,
    SUCCESS_COLOR,
    WAIT_MESSAGE,
)
from discord import Embed
from discord.ext import commands
from discord.ext.commands.context import Context
from news_utils import get_news


class NewsBot(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bot = bot

    @commands.command(name="news")
    async def news(self, ctx: Context, count: int = 3, confirmation: bool = False):
        if count <= 0:
            embed = Embed(
                title="❌ Ошибка!",
                description="Не могу отправить так мало новостей",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
            return

        if count >= 20 and not confirmation:
            embed = Embed(
                title="❌ Ошибка!",
                description=(
                    f"Слишком много новостей, бот будет спамить\n"
                    f"Введите `{COMMAND_PREFIX}news {count} True` чтобы подтвердить команду"
                ),
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)
            return

        embed = Embed(
            title="🚀 Получаем новости…",
            description=WAIT_MESSAGE,
            color=REGULAR_COLOR,
        )
        message = await ctx.send(embed=embed)

        news = get_news(count)
        embed = Embed(
            title="Последние посты" if len(news) >= 2 else "Последний пост",
            color=SUCCESS_COLOR,
        )
        await message.edit(embed=embed)

        for link in news:
            await ctx.send(link)
