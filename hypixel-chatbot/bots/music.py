import calendar
import datetime
import os
import random
from pathlib import Path

from common import REGULAR_COLOR, SUCCESS_COLOR, COMMAND_PREFIX, WAIT_MESSAGE
from database.__all_models import Music
from database.db_session import create_session
from discord import Embed, File
from discord.ext import commands
from discord.ext.commands.context import Context

session = create_session()


MUSIC_TITLES = [
    "🎵 Вот ваша музыка",
    "🎵 Музыка",
    "🎵 Minecraft Music",
]

MUSIC_STATS_TITLES = [
    "🎵 Статистика музыки",
    "🎵 Музыкальная статистика",
]


def get_song(user_id: int, title: str, month, year) -> Music:
    """Gets song by params, if result is None, new music object will be created automatically"""
    song = (
        session.query(Music)
        .filter(
            (Music.user_id == user_id)
            & (Music.title == title)
            & (Music.month == month)
            & (Music.year == year)
        )
        .first()
    )

    if song is None:
        song = Music(user_id=user_id, title=title, month=month, year=year)
        session.add(song)
        session.commit()

    return song


def get_user_music(user_id: int, month, year) -> list:
    query = (
        session.query(Music)
        .filter(
            (Music.user_id == user_id) & (Music.month == month) & (Music.year == year)
        )
        .order_by(Music.count)
        .all()
    )
    return list(query)


def get_current_month_and_year() -> tuple:
    current_date = datetime.date.today()
    month = current_date.month
    year = current_date.year

    return month, year


def pump_stats(user_id: int, music_title: str) -> None:
    month, year = get_current_month_and_year()
    user_song_all = get_song(
        user_id=user_id,
        title=music_title,
        month=None,
        year=None,
    )
    user_song_month = get_song(
        user_id=user_id,
        title=music_title,
        month=month,
        year=year,
    )
    all_song_all = get_song(
        user_id=-1,
        title=music_title,
        month=None,
        year=None,
    )
    all_song_month = get_song(
        user_id=-1,
        title=music_title,
        month=month,
        year=year,
    )

    user_song_all.count += 1
    user_song_month.count += 1
    all_song_all.count += 1
    all_song_month.count += 1

    session.commit()


def generate_stats_description(music_query):
    count = sum((song.count for song in music_query))
    count_str = f"Количество: {count}"
    top_3_title = f"Топ {min(count, 3)}:" if count else ""
    top_3 = (f"* {song.title}" for song in music_query[:3])

    return "\n".join((count_str, top_3_title, *top_3))


class MusicBot(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bot = bot

    @commands.group(name="music")
    async def music(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            file_path = Path("music/" + random.choice(os.listdir("music/")))
            file = File(file_path.absolute())

            user_id = ctx.author.id
            music_title = file_path.stem

            embed = Embed(
                title="🚀 Отправляем музыку…",
                description=WAIT_MESSAGE,
                color=REGULAR_COLOR,
            )
            message = await ctx.send(embed=embed)
            await ctx.send(file=file)
            embed = Embed(
                title=random.choice(MUSIC_TITLES),
                description=music_title,
                color=SUCCESS_COLOR,
            )
            embed.set_footer(text=f"Статистика — {COMMAND_PREFIX}music stats")
            await message.edit(embed=embed)

            pump_stats(user_id, music_title)

    @music.command()
    async def stats(self, ctx: Context):
        user_id = ctx.author.id
        month, year = get_current_month_and_year()
        month_name = calendar.month_name[month]

        user_song_all = get_user_music(user_id=user_id, month=None, year=None)
        user_song_month = get_user_music(user_id=user_id, month=month, year=year)
        all_song_all = get_user_music(user_id=-1, month=None, year=None)
        all_song_month = get_user_music(user_id=-1, month=month, year=year)

        embed = Embed(
            title=random.choice(MUSIC_STATS_TITLES),
            color=SUCCESS_COLOR,
        )

        # User
        embed.add_field(
            name=f"Ваша музыка за {month_name}",
            value=generate_stats_description(user_song_month),
            inline=False,
        )
        embed.add_field(
            name="Ваша музыка за всё время",
            value=generate_stats_description(user_song_all),
            inline=False,
        )

        # All
        embed.add_field(
            name=f"Вся музыка за {month_name}",
            value=generate_stats_description(all_song_month),
            inline=False,
        )
        embed.add_field(
            name="Вся музыка за всё время",
            value=generate_stats_description(all_song_all),
            inline=False,
        )
        await ctx.send(embed=embed)
