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

locale.setlocale(locale.LC_ALL, "ru_RU")


ONLINE_MESSAGES = [
    "Бот теперь онлайн",
    "Бот запущен",
]
OFFLINE_MESSAGES = [
    "Бот теперь оффлайн",
    "Бот отключен",
]


class HypixelBot(commands.Bot):
    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        user_id = message.author.id
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            user = User(id=user_id)
            session.add(user)
            session.commit()

        return await super().on_message(message)

    async def on_ready(self):
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
        if isinstance(exception, commands.CommandNotFound):
            embed = discord.Embed(
                title=ERROR_MESSAGE,
                description="Неизвестная команда",
                color=ERROR_COLOR,
            )
            await context.send(embed=embed)


def setup_logging():
    logger = logging.getLogger("discord")
    logger.setLevel(logging.WARNING)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)


def start_bot():
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

    bot.remove_command("help")

    @bot.command()
    async def help(context):
        embed = discord.Embed(
            title="❓ Помощь",
            description=(
                f"HypixelBot включает в себя четыре части:\n"
                f"• `StatsBot` — бот для статистики игроков Hypixel\n"
                f"• `MusicBot` — бот с музыкой из Майнкрафта\n"
                f"• `NewsBot` — бот с последними новостями Hypixel\n"
                f"• `SettingsBot` — бот для настройки\n"
                f"\n"
                f"Команды, доступные в StatsBot:\n"
                f"• `!stats <никнейм>` — основная статистика\n"
                f"• `!names <никнейм>` — история никнеймов\n"
                f"• `!socials <никнейм>` — социальные сети\n"
                f"• `!arcade <никнейм>` — статистика Arcade Games\n"
                f"• `!bw <никнейм>` — статистика Bed Wars\n"
                f"• `!duels <никнейм>` — статистика Duels\n"
                f"• `!paintball <никнейм>` — статистика Paintball\n"
                f"• `!tkr <никнейм>` — статистика Turbo Kart Racers\n"
                f"• `!guild <название>` — статистика гильдии\n"
                f"\n"
                f"Команды, доступные в MusicBot:\n"
                f"• `!music` — рандомная музыка из Майнкрафта\n"
                f"• `!music stats` — статистика музыки\n"
                f"\n"
                f"Команды, доступные в NewsBot:\n"
                f"• `!news` — последние 3 новости\n"
                f"• `!news <количество>` — последние новости в указанном количестве\n"
                f"\n"
                f"Команды, доступные в SettingsBot:\n"
                f"• `!settings` — настройки бота"
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
    setup_logging()
    start_bot()


if __name__ == "__main__":
    session = create_session()

    main()
