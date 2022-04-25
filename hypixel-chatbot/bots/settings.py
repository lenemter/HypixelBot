from common import COMMAND_PREFIX, REGULAR_COLOR, SUCCESS_COLOR, LOADING_EMBED
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


def bool_to_message(status: bool) -> str:
    return "Включено" if status else "Выключено"


def add_field_notification(embed: Embed, channel_id: int) -> Embed:
    chat_notifier = get_chat_notifier(channel_id)
    notifier_status = chat_notifier is not None

    embed.add_field(
        name=("🔔" if notifier_status else "🔕") + " Уведомления о запуске/остановке",
        value=(
            bool_to_message(notifier_status)
            + "\n"
            + f"`{COMMAND_PREFIX}settings notification`\n"
        ),
        inline=True,
    )

    return embed


def toggle_notifier(user_id: int, channel_id: int) -> None:
    chat_notifier = get_chat_notifier(channel_id)

    if chat_notifier is None:
        chat_notifier = ChatNotifier(user_id=user_id, channel_id=channel_id)
        session.add(chat_notifier)
    else:
        session.delete(chat_notifier)

    session.commit()


class SettingsBot(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bot = bot

    @commands.group(name="settings")
    async def settings(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            channel_id = ctx.channel.id

            message = await ctx.send(embed=LOADING_EMBED)
            embed = Embed(
                title="⚙️ Настройки",
                color=REGULAR_COLOR,
            )
            embed = add_field_notification(embed, channel_id)

            await message.edit(embed=embed)

    @settings.command()
    async def notification(self, ctx: Context):
        user_id = ctx.author.id
        channel_id = ctx.channel.id

        message = await ctx.send(embed=LOADING_EMBED)

        toggle_notifier(user_id, channel_id)

        embed = Embed(
            title="✅ Сохранено",
            color=SUCCESS_COLOR,
        )
        embed = add_field_notification(embed, channel_id)

        await message.edit(embed=embed)
