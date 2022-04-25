import calendar
import datetime

from discord.colour import Color
from discord import Embed

TOKEN = "OTYxNTQ5MTE5OTc1OTk3NDYy.Yk6mZg.CdomTHWPthQYL9tjoiRXs4HKwV8"
API_KEY = "81861188-cb9c-4392-a938-f5ca499e81a3"
DATABASE_PATH = "database/database.db"

# Colors
REGULAR_COLOR = Color.gold()
SUCCESS_COLOR = Color.green()
ERROR_COLOR = Color.red()

COMMAND_PREFIX = "!"
ACTIVITY_STATUS = f"{COMMAND_PREFIX}help"

ERROR_MESSAGE = "❌ Ошибка!"

WAIT_TITLE = "🚀 Загрузка…"
WAIT_MESSAGE = "Это может занять некоторое время"
LOADING_EMBED = Embed(
    title=WAIT_TITLE,
    description=WAIT_MESSAGE,
    color=REGULAR_COLOR,
)


def get_current_month_and_year() -> tuple:
    current_date = datetime.date.today()
    month = current_date.month
    year = current_date.year

    return month, year


def num_to_month(num: int):
    return calendar.month_name[num]
