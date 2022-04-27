from common import (
    COMMAND_PREFIX,
    ERROR_COLOR,
    ERROR_MESSAGE,
    LOADING_EMBED,
    SUCCESS_COLOR,
    get_current_month_and_year,
    num_to_month,
)
from database.__all_models import NewsRequest, NewsStats
from database.db_session import create_session
from discord import Embed
from discord.ext import commands
from discord.ext.commands.context import Context
from news_utils import get_news

session = create_session()


def get_news_stats(user_id: int, month, year) -> NewsStats:
    """Возвращает статистику новостей из БД по параметрам, если ничего не найдено, то новая запись в БД создаётся автоматически"""
    news_stats = (
        session.query(NewsStats)
        .filter(
            (NewsStats.user_id == user_id)
            & (NewsStats.month == month)
            & (NewsStats.year == year)
        )
        .first()
    )

    if news_stats is None:
        news_stats = NewsStats(user_id=user_id, month=month, year=year)
        session.add(news_stats)
        session.commit()

    return news_stats


def count_request(user_id: int, count: int) -> None:
    """Записывает статистику"""
    news_request = NewsRequest(user_id=user_id, count=count)
    session.add(news_request)

    month, year = get_current_month_and_year()
    user_news_all = get_news_stats(
        user_id=user_id,
        month=None,
        year=None,
    )
    user_news_month = get_news_stats(
        user_id=user_id,
        month=month,
        year=year,
    )
    all_news_all = get_news_stats(
        user_id=-1,
        month=None,
        year=None,
    )
    all_news_month = get_news_stats(
        user_id=-1,
        month=month,
        year=year,
    )

    user_news_all.count += 1
    user_news_month.count += 1
    all_news_all.count += 1
    all_news_month.count += 1

    session.commit()


def is_num(string: str) -> bool:
    """Проверка на число"""
    try:
        int(string)
        return True
    except Exception:
        return False


def generate_stats_description(news_stats) -> str:
    """Генерирует описания"""
    count = news_stats.count
    count_str = f"Количество: {count}"

    return count_str


class NewsBot(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bot = bot

    @commands.command(name="news")
    async def news(self, ctx: Context, count: str = "3", confirmation: bool = False):
        """!news <количество>"""
        if count == "stats":
            await self.stats(ctx)
        elif is_num(count):
            message = await ctx.send(embed=LOADING_EMBED)

            count = int(count)
            if count <= 0:
                embed = Embed(
                    title=ERROR_MESSAGE,
                    description="Не могу отправить так мало новостей",
                    color=ERROR_COLOR,
                )
                await message.edit(embed=embed)
                return

            if count >= 20 and not confirmation:
                embed = Embed(
                    title=ERROR_MESSAGE,
                    description=(
                        f"Слишком много новостей, бот будет спамить\n"
                        f"Введите `{COMMAND_PREFIX}news {count} True` чтобы подтвердить команду"
                    ),
                    color=ERROR_COLOR,
                )
                await message.edit(embed=embed)
                return

            news = get_news(count)
            embed = Embed(
                title="🗞 "
                + ("Последние посты" if len(news) >= 2 else "Последний пост"),
                color=SUCCESS_COLOR,
            )
            embed.set_footer(text=f"Статистика — {COMMAND_PREFIX}news stats")
            await message.edit(embed=embed)

            for link in news:
                await ctx.send(link)

            user_id = ctx.author.id
            count_request(user_id, count)
        else:
            embed = Embed(
                title=ERROR_MESSAGE,
                description="Неизвестный параметр",
                color=ERROR_COLOR,
            )
            await message.edit(embed=embed)

    async def stats(self, ctx: Context):
        """!news stats"""
        message = await ctx.send(embed=LOADING_EMBED)

        user_id = ctx.author.id
        month, year = get_current_month_and_year()
        month_name = num_to_month(month)

        user_news_all = get_news_stats(user_id=user_id, month=None, year=None)
        user_news_month = get_news_stats(user_id=user_id, month=month, year=year)
        all_news_all = get_news_stats(user_id=-1, month=None, year=None)
        all_news_month = get_news_stats(user_id=-1, month=month, year=year)

        embed = Embed(
            title="🗞 Статистика по новостям",
            color=SUCCESS_COLOR,
        )

        # User
        embed.add_field(
            name=f"Ваши запросы новосей за {month_name}",
            value=generate_stats_description(user_news_month),
            inline=False,
        )
        embed.add_field(
            name="Ваши запросы новостей за всё время",
            value=generate_stats_description(user_news_all),
            inline=False,
        )

        # All
        embed.add_field(
            name=f"Все запросы новостей за {month_name}",
            value=generate_stats_description(all_news_month),
            inline=False,
        )
        embed.add_field(
            name="Все запросы новостей за всё время",
            value=generate_stats_description(all_news_all),
            inline=False,
        )
        await message.edit(embed=embed)
