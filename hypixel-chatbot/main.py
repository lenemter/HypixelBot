import discord
from discord.ext import commands
import logging
import sqlalchemy

from common import TOKEN, COMMAND_PREFIX
from bots.news import News
from bots.news_reminder import NewsReminder
from bots.hypixel_stats import HypixelStats
from bots.music import Music
from database.db_session import global_init, create_session
from database.__all_models import User


global_init("database/database.db")
session = create_session()


class HypixelBot(commands.Bot):
    async def on_message(self, message: discord.Message):
        user_id = message.author.id
        user = User(id=user_id)
        try:
            session.add(user)
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            pass

        return await super().on_message(message)


def setup_logging():
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)


def start_bot():
    intents = discord.Intents.default()
    intents.members = True

    bot = HypixelBot(command_prefix=COMMAND_PREFIX, intents=intents)

    bot.add_cog(News(bot))
    bot.add_cog(NewsReminder(bot))
    bot.add_cog(HypixelStats(bot))
    bot.add_cog(Music(bot))

    bot.run(TOKEN)


def main():
    setup_logging()
    start_bot()


if __name__ == "__main__":
    main()
