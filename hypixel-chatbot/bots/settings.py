from common import COMMAND_PREFIX, REGULAR_COLOR, SUCCESS_COLOR
from database.__all_models import ChatNotifier
from database.db_session import create_session
from discord import Embed
from discord.ext import commands
from discord.ext.commands.context import Context

session = create_session()


def get_chat_notifier(channel_id: int):
    chat_notifier = (
        session.query(ChatNotifier)
        .filter(ChatNotifier.channel_id == channel_id)
        .first()
    )

    return chat_notifier


class SettingsBot(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bot = bot

    @commands.group(name="settings")
    async def settings(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            channel_id = ctx.channel.id

            embed = Embed(
                title="Настройки",
                color=REGULAR_COLOR,
            )

            chat_notifier = get_chat_notifier(channel_id)
            embed.add_field(
                name="Уведомления о запуске/остановке",
                value=(
                    f"`{COMMAND_PREFIX}settings notification`\n"
                    + str(chat_notifier is not None)
                ),
                inline=True,
            )

            await ctx.send(embed=embed)

    @settings.command()
    async def notification(self, ctx: Context):
        user_id = ctx.author.id
        channel_id = ctx.channel.id
        chat_notifier = get_chat_notifier(channel_id)

        if chat_notifier is None:
            chat_notifier = ChatNotifier(user_id=user_id, channel_id=channel_id)
            session.add(chat_notifier)
        else:
            session.delete(chat_notifier)

        session.commit()

        embed = Embed(
            title="Сохранено",
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)
