import hypixel
from common import API_KEY, COLOR, COMMAND_PREFIX, ERROR_COLOR, SUCCESS_COLOR
from discord import Embed
from discord.ext import commands
from discord.ext.commands.context import Context
from hypixel import HypixelException
from datetime import datetime


class HypixelStats(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bot = bot

    @commands.group(name="stats")
    async def get_stats(self, ctx: Context, where: str = ""):
        if not where:
            where = ctx.message.author.name

        where = where.lower()

        client = hypixel.Client(API_KEY)
        async with client:
            try:
                player = await client.player(where)
                friends = await client.player_friends(where)
                guild = client.guild_by_player(where)
            except HypixelException:
                embed = Embed(
                    title=f"❌ Ошибка!",
                    description=(f"Такого игрока не существует"),
                    color=ERROR_COLOR,
                )
                await ctx.send(embed=embed)

        last_login = player.last_login
        if last_login:
            last_login = player.last_login.strftime('%d.%m.%Y %H:%M:%S')
        else:
            last_login = "Скрыт в Hypixel API"

        embed = Embed(
            title=f"✅ Статистика {player.name}",
            description=(
                f"Ранг: {player.rank}\n"
                f"Уровень: {'{:,}'.format(player.level).replace(',', ' ')}\n"
                f"Очки достижений: {'{:,}'.format(player.achievement_points).replace(',', ' ')}\n"
                f"Карма: {'{:,}'.format(player.karma).replace(',', ' ')}\n"
                f"Количество друзей: {'{:,}'.format(len(friends)).replace(',', ' ')}\n\n"
                # f"Гильдия: {guild.name}\n\n"
                f"Первый вход: {player.first_login.strftime('%d.%m.%Y %H:%M:%S')}\n"
                f"Последний вход: {last_login}"
            ),
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)
