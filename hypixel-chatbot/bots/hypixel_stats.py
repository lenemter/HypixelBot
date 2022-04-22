import hypixel
from common import API_KEY, COLOR, COMMAND_PREFIX, ERROR_COLOR, SUCCESS_COLOR
from discord import Embed
from discord.ext import commands
from discord.ext.commands.context import Context
from hypixel import HypixelException
from stats_utils import format_date, format_number


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
                # guild = client.guild_by_player(where)
            except HypixelException:
                embed = Embed(
                    title=f"❌ Ошибка!",
                    description=(f"Такого игрока не существует"),
                    color=ERROR_COLOR,
                )
                await ctx.send(embed=embed)

        last_login = player.last_login
        if last_login:
            last_login = format_date(player.last_login)
        else:
            last_login = "Скрыт в Hypixel API"

        embed = Embed(
            title=f"📊 Статистика {player.name}",
            description=(
                f"Ранг: {player.rank}\n"
                f"Уровень: {format_number(player.level)}\n"
                f"Очки достижений: {format_number(player.achievement_points)}\n"
                f"Карма: {format_number(player.karma)}\n"
                f"Количество друзей: {format_number(len(friends))}\n\n"
                # f"Гильдия: {guild.name}\n\n"
                f"Первый вход: {format_date(player.first_login)}\n"
                f"Последний вход: {last_login}"
            ),
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)

    @commands.group(name="bw")
    async def get_bw(self, ctx: Context, where: str = ""):
        if not where:
            where = ctx.message.author.name

        where = where.lower()

        client = hypixel.Client(API_KEY)
        async with client:
            try:
                player = await client.player(where)
            except HypixelException:
                embed = Embed(
                    title=f"❌ Ошибка!",
                    description=(f"Такого игрока не существует"),
                    color=ERROR_COLOR,
                )
                await ctx.send(embed=embed)

        if not player.bedwars.winstreak:
            player_bedwars_winstreak = 0
        player_bedwars_winstreak = player.bedwars.winstreak

        embed = Embed(
            title=f"📊 Bed Wars статистика {player.name}",
            description=(
                f"Уровень: {format_number(player.bedwars.level)}\n\n"
                f"Киллы: {format_number(player.bedwars.kills)}\n"
                f"Смерти: {format_number(player.bedwars.deaths)}\n"
                f"KDR: {format_number(player.bedwars.kdr)}\n\n"
                f"Финальные киллы: {format_number(player.bedwars.final_kills)}\n"
                f"Финальные смерти: {format_number(player.bedwars.final_deaths)}\n"
                f"FKDR: {format_number(player.bedwars.fkdr)}\n\n"
                f"Победы: {format_number(player.bedwars.wins)}\n"
                f"Проигрыши: {format_number(player.bedwars.losses)}\n"
                f"WLR: {format_number(player.bedwars.wlr)}\n\n"
                f"Игр сыграно: {format_number(player.bedwars.games_played)}\n\n"
                f"Побед подряд: {format_number(player_bedwars_winstreak)}\n\n"
                f"Кроватей сломано: {format_number(player.bedwars.beds_broken)}\n"
                f"Кроватей потеряно: {format_number(player.bedwars.beds_lost)}\n"
                f"BBLR: {format_number(player.bedwars.bblr)}\n\n"
                f"Коины: {format_number(player.bedwars.coins)}"
            ),
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)
