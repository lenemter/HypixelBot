import hypixel
from common import API_KEY, ERROR_COLOR, SUCCESS_COLOR
from discord import Embed
from discord.ext import commands
from discord.ext.commands.context import Context
from hypixel import HypixelException
from stats_utils import create_head, format_date, format_number, round_number


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
            except HypixelException:
                embed = Embed(
                    title=f"❌ Ошибка!",
                    description=(f"Такого игрока не существует"),
                    color=ERROR_COLOR,
                )
                await ctx.send(embed=embed)

        player_uuid = player.uuid

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

        embed = Embed(
            title=f"📊 Статистика {player.name}",
            description=(
                f"Ранг: {player.rank}\n"
                f"\n"
                f"Уровень: {format_number(player.level)}\n"
                f"Ачивки: {format_number(player.achievement_points)}\n"
                f"Карма: {format_number(player.karma)}\n"
                f"\n"
                f"Друзья: {format_number(len(friends))}\n"
                f"\n"
                f"Первый вход: {format_date(player.first_login)}\n"
                f"Последний вход: {last_login}\n"
                f"Последняя игра: {last_game}"
            ),
            color=SUCCESS_COLOR,
        )
        embed.set_thumbnail(url=create_head(player_uuid))

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

        player_uuid = player.uuid

        names = [name for name in player.known_aliases]
        names.reverse()

        embed = Embed(
            title=f"📊 История никнеймов {player.name}",
            description=(
                "\n".join((f"{names.index(name) + 1}. {name}" for name in names))
            ),
            color=SUCCESS_COLOR,
        )
        embed.set_thumbnail(url=create_head(player_uuid))

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

        player_uuid = player.uuid

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
        embed.set_thumbnail(url=create_head(player_uuid))

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

        player_uuid = player.uuid

        if not player.bedwars.winstreak:
            player_bedwars_winstreak = 0
        else:
            player_bedwars_winstreak = player.bedwars.winstreak

        embed = Embed(
            title=f"📊 Bed Wars статистика {player.name}",
            description=(
                f"Уровень: {format_number(player.bedwars.level)}✫\n"
                f"\n"
                f"Киллы: {format_number(player.bedwars.kills)}\n"
                f"Смерти: {format_number(player.bedwars.deaths)}\n"
                f"K/D: {format_number(player.bedwars.kdr)}\n"
                f"\n"
                f"Финальные киллы: {format_number(player.bedwars.final_kills)}\n"
                f"Финальные смерти: {format_number(player.bedwars.final_deaths)}\n"
                f"FK/D: {format_number(player.bedwars.fkdr)}\n"
                f"\n"
                f"Победы: {format_number(player.bedwars.wins)}\n"
                f"Поражения: {format_number(player.bedwars.losses)}\n"
                f"W/L: {format_number(player.bedwars.wlr)}\n"
                f"\n"
                f"Сыгранные игры: {format_number(player.bedwars.games_played)}\n"
                f"\n"
                f"Победы подряд: {format_number(player_bedwars_winstreak)}\n"
                f"\n"
                f"Сломанные кровати: {format_number(player.bedwars.beds_broken)}\n"
                f"Потерянные кровати: {format_number(player.bedwars.beds_lost)}\n"
                f"BB/L: {format_number(player.bedwars.bblr)}\n"
                f"\n"
                f"Монеты: {format_number(player.bedwars.coins)}"
            ),
            color=SUCCESS_COLOR,
        )
        embed.set_thumbnail(url=create_head(player_uuid))

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

        player_uuid = player.uuid

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
                f"K/D: {format_number(player_duels_kdr)}\n"
                f"\n"
                f"Победы: {format_number(player.duels.wins)}\n"
                f"Поражения: {format_number(player.duels.losses)}\n"
                f"W/L: {format_number(player.duels.wlr)}\n"
                f"\n"
                f"Удары в ближнем бою: {format_number(player.duels.melee_hits)}\n"
                f"Попадания в ближнем бою: {format_number(player.duels.melee_swings)}\n"
                f"H/M: {format_number(player_duels_mhmr)}\n"
                f"\n"
                f"Выстрелы из лука: {format_number(player.duels.arrows_shot)}\n"
                f"Попадания с лука: {format_number(player.duels.arrows_hit)}\n"
                f"H/M: {format_number(player_duels_bhmr)}\n"
                f"\n"
                f"Монеты: {format_number(player.duels.coins)}"
            ),
            color=SUCCESS_COLOR,
        )
        embed.set_thumbnail(url=create_head(player_uuid))

        await ctx.send(embed=embed)

    @commands.group(name="arcade")
    async def get_arcade(self, ctx: Context, where: str = ""):
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

        player_uuid = player.uuid

        embed = Embed(
            title=f"📊 Arcade статистика {player.name}",
            description=(
                f"Монеты: {format_number(player.arcade.coins)}\n"
                f"\n"
                f"Hypixel Says:\n"
                f"Игр сыграно: {format_number(player.arcade.hypixel_says.rounds)}\n"
                f"Победы: {format_number(player.arcade.hypixel_says.wins)}\n"
                f"Проигрыши: {format_number(player.arcade.hypixel_says.losses)}\n"
                f"W/L: {format_number(player.arcade.hypixel_says.wlr)}\n"
                f"\n"
                f"Победы Party Games: {format_number(player.arcade.party_games.total_wins)}\n"
                f"\n"
                f"Capture The Wool:\n"
                f"Захваты шерсти: {format_number(player.arcade.ctw.captures)}\n"
                f"Киллы и ассисты: {format_number(player.arcade.ctw.kills_assists)}\n"
                f"\n"
                f"Mini Walls:\n"
                f"Победы: {format_number(player.arcade.mini_walls.wins)}\n"
                f"Киллы: {format_number(player.arcade.mini_walls.kills)}\n"
                f"Смерти: {format_number(player.arcade.mini_walls.deaths)}\n"
                f"K/D: {format_number(player.arcade.mini_walls.kdr)}\n"
                f"Финальные киллы: {format_number(player.arcade.mini_walls.final_kills)}\n"
                f"Киллы Иссушителя: {format_number(player.arcade.mini_walls.wither_kills)}\n"
                f"Урон Иссушителя: {format_number(player.arcade.mini_walls.wither_damage)}\n"
                f"Попадания стрелой: {format_number(player.arcade.mini_walls.arrows_hit)}\n"
                f"Общие выстрелы: {format_number(player.arcade.mini_walls.arrows_shot)}"
            ),
            color=SUCCESS_COLOR,
        )
        embed.set_thumbnail(url=create_head(player_uuid))

        await ctx.send(embed=embed)

    @commands.group(name="tkr")
    async def get_tkr(self, ctx: Context, where: str = ""):
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

        player_uuid = player.uuid

        embed = Embed(
            title=f"📊 Turbo Kart Racers статистика {player.name}",
            description=(
                f"Победы: {format_number(player.tkr.wins)}\n"
                f"\n"
                f"Пройденные круги: {format_number(player.tkr.laps)}\n"
                f"\n"
                f"Трофеи:\n"
                f"Золотые трофеи: {format_number(player.tkr.gold)}\n"
                f"Серебрянные трофеи: {format_number(player.tkr.silver)}\n"
                f"Бронзовые трофеи: {format_number(player.tkr.bronze)}\n"
                f"\n"
                f"Удары банановой шкуркой: {format_number(player.tkr.banana_hits)}\n"
                f"Наезды на банановую шкурку: {format_number(player.tkr.bananas_received)}\n"
                f"H/R: {format_number(player.tkr.br)}"
                f"\n"
                f"Удары синей торпедой: {format_number(player.tkr.blue_torpedo_hits)}\n"
                f"\n"
                f"Монеты: {format_number(player.tkr.coins)}"
            ),
            color=SUCCESS_COLOR,
        )
        embed.set_thumbnail(url=create_head(player_uuid))

        await ctx.send(embed=embed)

    @commands.group(name="paintball")
    async def get_paintball(self, ctx: Context, where: str = ""):
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

        player_uuid = player.uuid

        embed = Embed(
            title=f"📊 Paintball статистика {player.name}",
            description=(
                f"Победы: {format_number(player.paintball.wins)}\n"
                f"\n"
                f"Киллы: {format_number(player.paintball.kills)}\n"
                f"Серии киллов: {format_number(player.paintball.killstreaks)}\n"
                f"Смерти: {format_number(player.paintball.deaths)}\n"
                f"K/D: {format_number(player.paintball.kdr)}\n"
                f"\n"
                f"Выстрелы: {format_number(player.paintball.shots_fired)}\n"
                f"S/K: {format_number(player.paintball.skr)}\n"
                f"\n"
                f"Монеты: {format_number(player.paintball.coins)}"
            ),
            color=SUCCESS_COLOR,
        )
        embed.set_thumbnail(url=create_head(player_uuid))

        await ctx.send(embed=embed)
