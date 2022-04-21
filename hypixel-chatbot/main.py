import discord
from discord.ext import commands
import logging

from common import TOKEN, COMMAND_PREFIX
from bots.news import News
from bots.news_reminder import NewsReminder
from bots.hypixel_stats import HypixelStats
from bots.music import Music


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

    bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)
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
