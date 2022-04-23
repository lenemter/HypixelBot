import threading
import time

import schedule
from common import COMMAND_PREFIX, ERROR_COLOR, REGULAR_COLOR, SUCCESS_COLOR
from discord import Embed
from discord.ext import commands
from discord.ext.commands.context import Context


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() d oes not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


class NewsReminder(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bot = bot

        self.stop_run_continuously = None
        self.schedule_loop()

    def cog_unload(self):
        self.stop_run_continuously.set()
        return super().cog_unload()

    @commands.group(name="reminder")
    async def reminder(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            embed = Embed(
                title=f"{COMMAND_PREFIX}reminder",
                description=(
                    f"Использование:\n"
                    f"`"
                    f"{COMMAND_PREFIX}reminder set dm|chat\n"
                    f"{COMMAND_PREFIX}reminder remove dm|chat"
                    f"`"
                ),
                color=REGULAR_COLOR,
            )
            await ctx.send(embed=embed)

    @reminder.command()
    async def set(self, ctx: Context, where: str = ""):
        if not where:
            embed = Embed(
                title=f"{COMMAND_PREFIX}reminder set",
                description=(
                    f"Использование: `{COMMAND_PREFIX}reminder set dm|chat`\n"
                    f"dm   — Отправлять новости в Личные сообщения\n"
                    f"chat — Отправлять новости в этот чат"
                ),
                color=REGULAR_COLOR,
            )
            await ctx.send(embed=embed)
            return None

        where = where.lower()

        if where == "dm":
            embed = Embed(
                title="✅ Успешно!",
                description="Поставил оповещения в Личные сообщения.",
                color=SUCCESS_COLOR,
            )
            await ctx.send(embed=embed)
        elif where == "chat":
            embed = Embed(
                title="✅ Успешно!",
                description="Поставил оповещения в этот чат.",
                color=SUCCESS_COLOR,
            )
            await ctx.send(embed=embed)
        else:
            embed = Embed(
                title="❌ Ошибка!",
                description="Неизвестное место для оповещений.",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)

    @reminder.command()
    async def remove(self, ctx: Context, where: str = ""):
        if not where:
            embed = Embed(
                title=f"{COMMAND_PREFIX}reminder remove",
                description=(
                    f"Использование: `{COMMAND_PREFIX}reminder remove dm|chat`\n"
                    f"dm   — Не отправлять новости в Личные сообщения\n"
                    f"chat — Не отправлять новости в этот чат"
                ),
                color=REGULAR_COLOR,
            )
            await ctx.send(embed=embed)

            return None

        where = where.lower()

        if where == "dm":
            embed = Embed(
                title="✅ Успешно!",
                description="Удалил оповещения в Личные сообщения.",
                color=SUCCESS_COLOR,
            )
            await ctx.send(embed=embed)
        elif where == "chat":
            embed = Embed(
                title="✅ Успешно!",
                description="Удалил оповещения в этот чат.",
                color=SUCCESS_COLOR,
            )
            await ctx.send(embed=embed)
        else:
            embed = Embed(
                title="❌ Ошибка!",
                description="Неизвестное место для удаления.",
                color=ERROR_COLOR,
            )
            await ctx.send(embed=embed)

    def send_reminders(self):
        print("SUSSY BAKA ПРОБУДИЛСЯ")

    def schedule_loop(self):
        schedule.every().hour.at("06:00").do(self.send_reminders)
        self.stop_run_continuously = run_continuously()
