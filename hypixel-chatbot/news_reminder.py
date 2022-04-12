from discord.ext import commands
from discord.ext.commands.context import Context
import schedule
import threading
import time

from common import COMMAND_PREFIX


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
            await ctx.send(
                f"Использование:\n"
                f"{COMMAND_PREFIX}reminder set dm/chat\n"
                f"{COMMAND_PREFIX}reminder remove dm/chat"
            )

    @reminder.command()
    async def set(self, ctx: Context, where: str = ""):
        if not where:
            await ctx.send(
                f"Использование: {COMMAND_PREFIX}reminder set dm|chat\n"
                f"dm   — Отправлять новости в Личные сообщения\n"
                f"chat — Отправлять новости в этот чат"
            )
            return None

        where = where.lower()

        if where == "dm":
            await ctx.send("Поставил оповещения в Личные сообщения.")
        elif where == "chat":
            await ctx.send("Поставил оповещения в этот чат.")
        else:
            await ctx.send("Неизвестное место для оповещений.")

    @reminder.command()
    async def remove(self, ctx: Context, where: str = ""):
        if not where:
            await ctx.send(
                f"Использование: {COMMAND_PREFIX}reminder remove dm|chat\n"
                f"dm   — Не отправлять новости в Личные сообщения\n"
                f"chat — Не отправлять новости в этот чат"
            )
            return None

        where = where.lower()

        if where == "dm":
            await ctx.send("Удалил оповещения в Личные сообщения.")
        elif where == "chat":
            await ctx.send("Удалил оповещения в этот чат.")
        else:
            await ctx.send("Неизвестное место для удаления.")

    def send_reminders(self):
        pass

    def schedule_loop(self):
        # schedule.every().hour.at("00:00").do(self.send_reminders)
        schedule.every().second.do(self.send_reminders)
        self.stop_run_continuously = run_continuously()
