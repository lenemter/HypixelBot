import discord
from discord.ext import commands
import logging
import locale

from database.db_session import global_init, create_session
from database.__all_models import User, ChatNotifier
from common import TOKEN, COMMAND_PREFIX, DATABASE_PATH, ERROR_COLOR, SUCCESS_COLOR

# This is here for bots imports
global_init(DATABASE_PATH)

from bots.news import NewsBot
from bots.hypixel_stats import HypixelStats
from bots.music import MusicBot
from bots.settings import SettingsBot

locale.setlocale(locale.LC_ALL, "ru_RU")


class HypixelBot(commands.Bot):
    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        user_id = message.author.id
        user = session.query(User).filter(User.id == user_id)
        if not user:
            user = User(id=user_id)
            session.add(user)
            session.commit()

        return await super().on_message(message)

    async def on_ready(self):
        chat_notifiers = session.query(ChatNotifier)
        for chat_notifier in chat_notifiers:
            chat_id = chat_notifier.chat_id
            channel = self.get_channel(chat_id)

            embed = discord.Embed(title="Бот теперь онлайн", color=SUCCESS_COLOR)
            await channel.send(embed=embed)

    async def close(self):
        chat_notifiers = session.query(ChatNotifier)
        for chat_notifier in chat_notifiers:
            chat_id = chat_notifier.chat_id
            channel = self.get_channel(chat_id)

            embed = discord.Embed(title="Бот теперь оффлайн", color=ERROR_COLOR)
            await channel.send(embed=embed)

        return await super().close()


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

    bot = HypixelBot(command_prefix=COMMAND_PREFIX, intents=intents)

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
