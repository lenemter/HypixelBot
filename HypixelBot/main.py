import locale
import logging
import random

import discord
from discord.ext import commands

from common import (
    ACTIVITY_STATUS,
    COMMAND_PREFIX,
    DATABASE_PATH,
    ERROR_COLOR,
    ERROR_MESSAGE,
    SUCCESS_COLOR,
    TOKEN,
)
from database.__all_models import ChatNotifier, User
from database.db_session import create_session, global_init

# This is here for bots imports
global_init(DATABASE_PATH)

from bots.music import MusicBot
from bots.news import NewsBot
from bots.settings import SettingsBot
from bots.stats import HypixelStats

locale.setlocale(locale.LC_ALL, "C")


ONLINE_MESSAGES = [
    "Бот теперь онлайн",
    "Бот запущен",
]
OFFLINE_MESSAGES = [
    "Бот теперь оффлайн",
    "Бот отключен",
]


def setup_db() -> None:
    # Добавляет пользователя с id -1 в БД
    no_user_id = -1
    user = session.query(User).filter(User.id == no_user_id).first()
    if not user:
        user = User(id=no_user_id)
        session.add(user)
        session.commit()


def register_user(user_id: int) -> None:
    """Добавляет ползователя в БД"""
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id)
        session.add(user)
        session.commit()


class HypixelBot(commands.Bot):
    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        user_id = message.author.id
        register_user(user_id)

        return await super().on_message(message)

    async def on_ready(self):
        """При запуске бота, бот отправляет рандомное сообщение о запуске"""
        chat_notifiers = session.query(ChatNotifier)
        for chat_notifier in chat_notifiers:
            channel_id = chat_notifier.channel_id
            channel = self.get_channel(channel_id)

            embed = discord.Embed(
                title=random.choice(ONLINE_MESSAGES),
                color=SUCCESS_COLOR,
            )
            await channel.send(embed=embed)

    async def close(self):
        """При отключении бота, бот отправляет рандомное сообщение о выключении"""
        chat_notifiers = session.query(ChatNotifier)
        for chat_notifier in chat_notifiers:
            channel_id = chat_notifier.channel_id
            channel = self.get_channel(channel_id)

            embed = discord.Embed(
                title=random.choice(OFFLINE_MESSAGES),
                color=ERROR_COLOR,
            )
            await channel.send(embed=embed)

        return await super().close()

    async def on_command_error(self, context, exception):
        """Ошибка о неизвестной команде"""
        if isinstance(exception, commands.CommandNotFound):
            embed = discord.Embed(
                title=ERROR_MESSAGE,
                description="Неизвестная команда",
                color=ERROR_COLOR,
            )
            await context.send(embed=embed)


def setup_logging():
    """Настройки логирования"""
    logger = logging.getLogger("discord")
    logger.setLevel(logging.WARNING)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)


def start_bot():
    """Запуск бота"""
    intents = discord.Intents.default()
    intents.members = True

    activity = discord.Activity(
        name=ACTIVITY_STATUS,
        type=discord.ActivityType.playing,
    )
    bot = HypixelBot(
        command_prefix=COMMAND_PREFIX,
        intents=intents,
        activity=activity,
        help_command=None,
    )

    @bot.command()
    async def help(context):
        embed = discord.Embed(
            title="Помощь",
            description=(
                f"**HypixelBot — универсальный бот для Hypixel**\n"
                f"• **StatsBot** — бот для статистики Hypixel\n"
                f"• **MusicBot** — бот с музыкой из Minecraft\n"
                f"• **NewsBot** — бот с последними новостями Hypixel\n"
                f"• **SettingsBot** — бот для настройки\n"
                f"\n"
                f"Команды, доступные в **StatsBot**\n"
                f"• `{COMMAND_PREFIX}stats <никнейм>` — основная статистика\n"
                f"• `{COMMAND_PREFIX}names <никнейм>` — история никнеймов\n"
                f"• `{COMMAND_PREFIX}socials <никнейм>` — социальные сети\n"
                f"• `{COMMAND_PREFIX}arcade <никнейм>` — статистика Arcade Games\n"
                f"• `{COMMAND_PREFIX}bw <никнейм>` — статистика Bed Wars\n"
                f"• `{COMMAND_PREFIX}duels <никнейм>` — статистика Duels\n"
                f"• `{COMMAND_PREFIX}paintball <никнейм>` — статистика Paintball\n"
                f"• `{COMMAND_PREFIX}tkr <никнейм>` — статистика Turbo Kart Racers\n"
                f"• `{COMMAND_PREFIX}guild <название>` — статистика гильдии\n"
                f"• `{COMMAND_PREFIX}server` — статистика сервера\n"
                f"• `{COMMAND_PREFIX}skin <никнейм>` — скин игрока\n"
                f"\n"
                f"Команды, доступные в **MusicBot**\n"
                f"• `{COMMAND_PREFIX}music` — рандомная музыка из Майнкрафта\n"
                f"• `{COMMAND_PREFIX}music stats` — статистика музыки\n"
                f"\n"
                f"Команды, доступные в **NewsBot**\n"
                f"• `{COMMAND_PREFIX}news` — последние 3 новости\n"
                f"• `{COMMAND_PREFIX}news <количество>` — последние новости в указанном количестве\n"
                f"• `{COMMAND_PREFIX}news stats` — статистика по запросу новостей\n"
                f"\n"
                f"Команды, доступные в **SettingsBot**\n"
                f"• `{COMMAND_PREFIX}settings` — настройки бота"
            ),
            color=SUCCESS_COLOR,
        )
        await context.send(embed=embed)

    bot.add_cog(NewsBot(bot))
    bot.add_cog(HypixelStats(bot))
    bot.add_cog(MusicBot(bot))
    bot.add_cog(SettingsBot(bot))

    bot.run(TOKEN)


def main():
    setup_db()
    setup_logging()
    start_bot()


if __name__ == "__main__":
    session = create_session()

    main()
