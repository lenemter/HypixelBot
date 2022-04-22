import hypixel
from common import API_KEY, COLOR, COMMAND_PREFIX, ERROR_COLOR, SUCCESS_COLOR
from discord import Embed
from discord.ext import commands
from discord.ext.commands.context import Context
from hypixel import HypixelException
from stats_utils import format_date, format_number, round_number


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

        last_game = player.most_recent_game
        if not last_game:
            last_game = "Скрыта в Hypixel API"
        else:
            last_game = player.most_recent_game.clean_name

        active_gadget = player.current_gadget
        if not active_gadget:
            active_gadget = "—"
        else:
            active_gadget = player.current_gadget.capitalize()

        embed = Embed(
            title=f"📊 Статистика {player.name}",
            description=(
                f"Ранг: {player.rank}\n"
                f"Уровень: {format_number(player.level)}\n"
                f"Ачивки: {format_number(player.achievement_points)}\n"
                f"Карма: {format_number(player.karma)}\n"
                f"Друзья: {format_number(len(friends))}\n\n"
                # f"Гильдия: {guild.name}\n\n"
                f"Гаджет: {active_gadget}\n\n"
                f"Первый вход: {format_date(player.first_login)}\n"
                f"Последний вход: {last_login}\n"
                f"Последняя игра: {last_game}"
            ),
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)

    @commands.group(name="names")
    async def get_names(self, ctx: Context, where: str = ""):
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

        names = [name for name in player.known_aliases]
        names.reverse()

        embed = Embed(
            title=f"📊 История никнеймов {player.name}",
            description=(
                "\n".join((f"{names.index(name) + 1}. {name}" for name in names))
            ),
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)

    @commands.group(name="socials")
    async def get_socials(self, ctx: Context, where: str = ""):
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

        socials = dict()
        socials["Discord"] = player.socials.discord
        socials["YouTube"] = player.socials.youtube
        socials["Twitter"] = player.socials.twitter
        socials["Twitch"] = player.socials.twitch
        socials["Instagram"] = player.socials.instagram
        socials["Hypixel Forums"] = player.socials.hypixel_forums

        message_content = "\n".join(
            (f"{social}: {socials[social]}" for social in socials if socials[social])
        )
        if not message_content:
            message_content = "Социальные сети не указаны"

        embed = Embed(
            title=f"📊 Социальные сети {player.name}",
            description=(message_content),
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
        else:
            player_bedwars_winstreak = player.bedwars.winstreak

        embed = Embed(
            title=f"📊 Bed Wars статистика {player.name}",
            description=(
                f"Уровень: {format_number(player.bedwars.level)}✫\n\n"
                f"Киллы: {format_number(player.bedwars.kills)}\n"
                f"Смерти: {format_number(player.bedwars.deaths)}\n"
                f"K/D: {format_number(player.bedwars.kdr)}\n\n"
                f"Финальные киллы: {format_number(player.bedwars.final_kills)}\n"
                f"Финальные смерти: {format_number(player.bedwars.final_deaths)}\n"
                f"FK/D: {format_number(player.bedwars.fkdr)}\n\n"
                f"Победы: {format_number(player.bedwars.wins)}\n"
                f"Проигрыши: {format_number(player.bedwars.losses)}\n"
                f"W/L: {format_number(player.bedwars.wlr)}\n\n"
                f"Игр сыграно: {format_number(player.bedwars.games_played)}\n\n"
                f"Побед подряд: {format_number(player_bedwars_winstreak)}\n\n"
                f"Кроватей сломано: {format_number(player.bedwars.beds_broken)}\n"
                f"Кроватей потеряно: {format_number(player.bedwars.beds_lost)}\n"
                f"BB/L: {format_number(player.bedwars.bblr)}\n\n"
                f"Монеты: {format_number(player.bedwars.coins)}"
            ),
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)

    @commands.group(name="duels")
    async def get_duels(self, ctx: Context, where: str = ""):
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

        player_duels_kdr = round_number(player.duels.kills / player.duels.deaths)
        player_duels_mhmr = round_number(
            player.duels.melee_hits / player.duels.melee_swings
        )
        player_duels_bhmr = round_number(
            player.duels.arrows_hit / player.duels.arrows_shot
        )

        embed = Embed(
            title=f"📊 Duels статистика {player.name}",
            description=(
                f"Киллы: {format_number(player.duels.kills)}\n"
                f"Смерти: {format_number(player.duels.deaths)}\n"
                f"K/D: {format_number(player_duels_kdr)}\n\n"
                f"Победы: {format_number(player.duels.wins)}\n"
                f"Проигрыши: {format_number(player.duels.losses)}\n"
                f"W/L: {format_number(player.duels.wlr)}\n\n"
                f"Удары оружием: {format_number(player.duels.melee_hits)}\n"
                f"Попадания: {format_number(player.duels.melee_swings)}\n"
                f"H/M: {format_number(player_duels_mhmr)}\n\n"
                f"Выстрелы из лука: {format_number(player.duels.arrows_shot)}\n"
                f"Попадания: {format_number(player.duels.arrows_hit)}\n"
                f"H/M: {format_number(player_duels_bhmr)}\n\n"
                f"Монеты: {format_number(player.duels.coins)}"
            ),
            color=SUCCESS_COLOR,
        )
        await ctx.send(embed=embed)
