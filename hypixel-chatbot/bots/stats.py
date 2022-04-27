import hypixel
from common import (
    API_KEY,
    COMMAND_PREFIX,
    ERROR_COLOR,
    ERROR_MESSAGE,
    LOADING_EMBED,
    SUCCESS_COLOR,
)
from discord import Embed
from discord.ext import commands
from discord.ext.commands.context import Context
from hypixel import HypixelException
from stats_utils import (
    create_avatar,
    create_head,
    create_skin,
    floor_number,
    format_date,
    format_number,
    get_player_by_uuid,
    round_number,
)

HELP_FOOTER = f"Помощь — {COMMAND_PREFIX}help"
NO_SUCH_PLAYER_MESSAGE = "Такого игрока не существует"


class HypixelStats(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bot = bot

    @commands.command(name="stats")
    async def get_stats(self, ctx: Context, nickname: str = ""):
        message = await ctx.send(embed=LOADING_EMBED)

        if not nickname:
            nickname = ctx.message.author.name
        nickname = nickname.lower()

        client = hypixel.Client(API_KEY)
        async with client:
            try:
                player = await client.player(nickname)
                friends = await client.player_friends(nickname)
                player_status = await client.player_status(nickname)
            except HypixelException:
                embed = Embed(
                    title=ERROR_MESSAGE,
                    description=NO_SUCH_PLAYER_MESSAGE,
                    color=ERROR_COLOR,
                )
                embed.set_footer(
                    text=f"Использование — {COMMAND_PREFIX}stats <никнейм>"
                )
                await message.edit(embed=embed)
                return

            try:
                guild = await client.guild_by_player(nickname)
                guild_info = f"{guild.name} [{guild.tag}]"
            except HypixelException:
                guild_info = "—"

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

        status = player_status.online
        if status:
            status = f"На сервере — {player_status.game_type.clean_name}"
        else:
            status = "Оффлайн"

        player_rank_title = player.rank
        if player_rank_title:
            player_rank_title = f"[{player.rank}]"
        else:
            player_rank_title = ""

        embed = Embed(
            title=f"{player_rank_title} {player.name}",
            description=(
                f"Ранг: {player.rank}\n"
                f"\n"
                f"Уровень: {format_number(player.level)}\n"
                f"Ачивки: {format_number(player.achievement_points)}\n"
                f"Карма: {format_number(player.karma)}\n"
                f"\n"
                f"Друзья: {format_number(len(friends))}\n"
                f"Гильдия: {guild_info}\n"
                f"\n"
                f"Первый вход: {format_date(player.first_login)}\n"
                f"Последний вход: {last_login}\n"
                f"Последняя игра: {last_game}\n"
                f"\n"
                f"Статус: {status}"
            ),
            color=SUCCESS_COLOR,
        )

        embed.set_thumbnail(url=create_head(player_uuid))
        embed.set_footer(text=HELP_FOOTER)
        embed.set_author(
            name=f"Статистика {player.name}", icon_url=create_avatar(player_uuid)
        )

        await message.edit(embed=embed)

    @commands.command(name="skin")
    async def get_skin(self, ctx: Context, nickname: str = ""):
        message = await ctx.send(embed=LOADING_EMBED)

        if not nickname:
            nickname = ctx.message.author.name
        nickname = nickname.lower()

        client = hypixel.Client(API_KEY)
        async with client:
            try:
                player = await client.player(nickname)
            except HypixelException:
                embed = Embed(
                    title=ERROR_MESSAGE,
                    description=NO_SUCH_PLAYER_MESSAGE,
                    color=ERROR_COLOR,
                )
                embed.set_footer(text=f"Использование — {COMMAND_PREFIX}skin <никнейм>")
                await message.edit(embed=embed)
                return

        player_uuid = player.uuid

        embed = Embed(
            color=SUCCESS_COLOR,
        )

        embed.set_image(url=create_skin(player_uuid))
        embed.set_footer(text=HELP_FOOTER)
        embed.set_author(
            name=f"Скин {player.name}", icon_url=create_avatar(player_uuid)
        )

        await message.edit(embed=embed)

    @commands.command(name="server")
    async def get_server(self, ctx: Context, nickname: str = ""):
        message = await ctx.send(embed=LOADING_EMBED)

        client = hypixel.Client(API_KEY)
        async with client:
            try:
                player_count = await client.player_count()
                bans = await client.bans()
            except HypixelException:
                return

        embed = Embed(
            title=f"Hypixel Network — mc.hypixel.net",
            description=(
                f"Онлайн: {format_number(player_count)}\n"
                f"\n"
                f"Статистика банов:\n"
                f"Watchdog за всё время: {format_number(bans.watchdog_total)}\n"
                f"Watchdog за день: {format_number(bans.watchdog_day)}\n"
                f"Watchdog недавние: {format_number(bans.watchdog_recent)}\n"
                f"Модераторы на всё время: {format_number(bans.staff_total)}\n"
                f"Модераторы за день: {format_number(bans.staff_day)}"
            ),
            color=SUCCESS_COLOR,
        )

        embed.set_footer(text=HELP_FOOTER)
        embed.set_author(
            name=f"Статистика сервера",
            icon_url="https://dl.labymod.net/img/server/hypixel/icon@2x.webp",
        )

        await message.edit(embed=embed)

    @commands.command(name="names")
    async def get_names(self, ctx: Context, nickname: str = ""):
        message = await ctx.send(embed=LOADING_EMBED)

        if not nickname:
            nickname = ctx.message.author.name
        nickname = nickname.lower()

        client = hypixel.Client(API_KEY)
        async with client:
            try:
                player = await client.player(nickname)
            except HypixelException:
                embed = Embed(
                    title=ERROR_MESSAGE,
                    description=NO_SUCH_PLAYER_MESSAGE,
                    color=ERROR_COLOR,
                )
                embed.set_footer(
                    text=f"Использование — {COMMAND_PREFIX}names <никнейм>"
                )
                await message.edit(embed=embed)
                return

        player_uuid = player.uuid

        names = [name for name in player.known_aliases]
        names.reverse()

        embed = Embed(
            title=f"{player.name}",
            description=(
                "\n".join((f"{names.index(name) + 1}. {name}" for name in names))
            ),
            color=SUCCESS_COLOR,
        )

        embed.set_thumbnail(url=create_head(player_uuid))
        embed.set_footer(text=HELP_FOOTER)
        embed.set_author(
            name=f"История никнеймов {player.name}", icon_url=create_avatar(player_uuid)
        )

        await message.edit(embed=embed)

    @commands.command(name="socials")
    async def get_socials(self, ctx: Context, nickname: str = ""):
        message = await ctx.send(embed=LOADING_EMBED)

        if not nickname:
            nickname = ctx.message.author.name
        nickname = nickname.lower()

        client = hypixel.Client(API_KEY)
        async with client:
            try:
                player = await client.player(nickname)
            except HypixelException:
                embed = Embed(
                    title=ERROR_MESSAGE,
                    description=NO_SUCH_PLAYER_MESSAGE,
                    color=ERROR_COLOR,
                )
                embed.set_footer(
                    text=f"Использование — {COMMAND_PREFIX}socials <никнейм>"
                )
                await message.edit(embed=embed)
                return

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

        player_rank_title = player.rank
        if player_rank_title:
            player_rank_title = f"[{player.rank}]"
        else:
            player_rank_title = ""

        embed = Embed(
            title=f"{player_rank_title} {player.name}",
            description=message_content,
            color=SUCCESS_COLOR,
        )

        embed.set_thumbnail(url=create_head(player_uuid))
        embed.set_footer(text=HELP_FOOTER)
        embed.set_author(
            name=f"Социальные сети {player.name}", icon_url=create_avatar(player_uuid)
        )

        await message.edit(embed=embed)

    @commands.command(name="guild")
    async def get_guild(self, ctx: Context, guild_name: str = ""):
        message = await ctx.send(embed=LOADING_EMBED)

        if not guild_name:
            embed = Embed(
                title=ERROR_MESSAGE,
                description="Введите название гильдии",
                color=ERROR_COLOR,
            )
            embed.set_footer(text=f"Использование — {COMMAND_PREFIX}guild <название>")
            await message.edit(embed=embed)
            return

        guild_name = guild_name.lower()

        client = hypixel.Client(API_KEY)
        async with client:
            try:
                guild = await client.guild_by_name(guild_name)
                guild_master = await client.player(
                    get_player_by_uuid(guild.members[0].uuid)
                )
            except HypixelException:
                embed = Embed(
                    title=ERROR_MESSAGE,
                    description="Такой гильдии не существует",
                    color=ERROR_COLOR,
                )
                embed.set_footer(
                    text=f"Использование — {COMMAND_PREFIX}guild <название>"
                )
                await message.edit(embed=embed)
                return

        description = guild.description
        if not description:
            description = "—"

        guild_tag = guild.tag
        if not guild_tag:
            guild_tag = "—"
        else:
            guild_tag = f"[{guild.tag}]"

        guild_tag_title = guild.tag
        if not guild_tag_title:
            guild_tag_title = ""
        else:
            guild_tag_title = f"[{guild.tag}]"

        guild_master_rank = guild_master.rank
        if not guild_master_rank:
            guild_master_rank = ""
        else:
            guild_master_rank = f"[{guild_master.rank}]"

        tag_color = guild.tag_color
        if not tag_color:
            tag_color = "Серый"
        elif tag_color.clean_name == "Dark-Aqua":
            tag_color = "Бирюзовый"
        elif tag_color.clean_name == "Dark-Green":
            tag_color = "Тёмно-зеленый"
        elif tag_color.clean_name == "Yellow":
            tag_color = "Жёлтый"
        elif tag_color.clean_name == "Gold":
            tag_color = "Золотой"

        publically_listed = guild.publicly_listed
        if publically_listed:
            publically_listed = "Да"
        else:
            publically_listed = "Нет"

        joinable = guild.joinable
        if joinable:
            joinable = "Да"
        else:
            joinable = "Нет"

        favorite_games = []
        for game in guild.preferred_games:
            favorite_games.append(game.clean_name)
        if not favorite_games:
            favorite_games.append("—")

        embed = Embed(
            title=f"{guild.name} {guild_tag_title}",
            description=(
                f"Название: {guild.name}\n"
                f"Тэг: {guild_tag}\n"
                f"Цвет тэга: {tag_color}\n"
                f"\n"
                f"Описание:\n{description}\n"
                f"\n"
                f"Уровень: {format_number(floor_number(guild.level))}"
                f"\n"
                f"Глава гильдии: {guild_master_rank} {guild_master.name}\n"
                f"Участники: {format_number(len(guild.members))}\n"
                f"\n"
                f"Создана: {format_date(guild.created)}\n"
                f"\n"
                f"Опыт гильдии: {format_number(guild.exp)}\n"
                f"\n"
                f"Публичная: {publically_listed}\n"
                f"Открытая: {joinable}\n"
                f"\n"
                f"Любимые игры: {', '.join(favorite_games)}"
            ),
            color=SUCCESS_COLOR,
        )

        embed.set_footer(text=HELP_FOOTER)
        embed.set_author(
            name=f"Гильдия {guild.name} {guild_tag_title}",
            icon_url="https://dl.labymod.net/img/server/hypixel/icon@2x.webp",
        )

        await message.edit(embed=embed)

    @commands.command(name="bw")
    async def get_bw(self, ctx: Context, nickname: str = ""):
        message = await ctx.send(embed=LOADING_EMBED)

        if not nickname:
            nickname = ctx.message.author.name
        nickname = nickname.lower()

        client = hypixel.Client(API_KEY)
        async with client:
            try:
                player = await client.player(nickname)
            except HypixelException:
                embed = Embed(
                    title=ERROR_MESSAGE,
                    description=NO_SUCH_PLAYER_MESSAGE,
                    color=ERROR_COLOR,
                )
                embed.set_footer(text=f"Использование — {COMMAND_PREFIX}bw <никнейм>")
                await message.edit(embed=embed)
                return

        player_uuid = player.uuid

        if not player.bedwars.winstreak:
            player_bedwars_winstreak = 0
        else:
            player_bedwars_winstreak = player.bedwars.winstreak

        player_rank_title = player.rank
        if player_rank_title:
            player_rank_title = f"[{player.rank}]"
        else:
            player_rank_title = ""

        embed = Embed(
            title=f"{player_rank_title} {player.name}",
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
        embed.set_footer(text=HELP_FOOTER)
        embed.set_author(
            name=f"Bed Wars статистика {player.name}",
            icon_url=create_avatar(player_uuid),
        )

        await message.edit(embed=embed)

    @commands.command(name="duels")
    async def get_duels(self, ctx: Context, nickname: str = ""):
        message = await ctx.send(embed=LOADING_EMBED)

        if not nickname:
            nickname = ctx.message.author.name
        nickname = nickname.lower()

        client = hypixel.Client(API_KEY)
        async with client:
            try:
                player = await client.player(nickname)
            except HypixelException:
                embed = Embed(
                    title=ERROR_MESSAGE,
                    description=NO_SUCH_PLAYER_MESSAGE,
                    color=ERROR_COLOR,
                )
                embed.set_footer(
                    text=f"Использование — {COMMAND_PREFIX}duels <никнейм>"
                )
                await message.edit(embed=embed)
                return

        player_uuid = player.uuid

        player_duels_kdr = round_number(player.duels.kills / player.duels.deaths)

        player_duels_mhmr = round_number(
            player.duels.melee_hits / player.duels.melee_swings
        )

        player_duels_bhmr = round_number(
            player.duels.arrows_hit / player.duels.arrows_shot
        )

        player_rank_title = player.rank
        if player_rank_title:
            player_rank_title = f"[{player.rank}]"
        else:
            player_rank_title = ""

        embed = Embed(
            title=f"{player_rank_title} {player.name}",
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
        embed.set_footer(text=HELP_FOOTER)
        embed.set_author(
            name=f"Duels статистика {player.name}", icon_url=create_avatar(player_uuid)
        )

        await message.edit(embed=embed)

    @commands.command(name="arcade")
    async def get_arcade(self, ctx: Context, nickname: str = ""):
        message = await ctx.send(embed=LOADING_EMBED)

        if not nickname:
            nickname = ctx.message.author.name
        nickname = nickname.lower()

        client = hypixel.Client(API_KEY)
        async with client:
            try:
                player = await client.player(nickname)
            except HypixelException:
                embed = Embed(
                    title=ERROR_MESSAGE,
                    description=NO_SUCH_PLAYER_MESSAGE,
                    color=ERROR_COLOR,
                )
                embed.set_footer(
                    text=f"Использование — {COMMAND_PREFIX}arcade <никнейм>"
                )
                await message.edit(embed=embed)
                return

        player_uuid = player.uuid

        player_rank_title = player.rank
        if player_rank_title:
            player_rank_title = f"[{player.rank}]"
        else:
            player_rank_title = ""

        embed = Embed(
            title=f"{player_rank_title} {player.name}",
            description=(
                f"Монеты: {format_number(player.arcade.coins)}\n"
                f"\n"
                f"Hypixel Says:\n"
                f"Игр сыграно: {format_number(player.arcade.hypixel_says.rounds)}\n"
                f"Победы: {format_number(player.arcade.hypixel_says.wins)}\n"
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
        embed.set_footer(text=HELP_FOOTER)
        embed.set_author(
            name=f"Arcade Games статистика {player.name}",
            icon_url=create_avatar(player_uuid),
        )

        await message.edit(embed=embed)

    @commands.command(name="tkr")
    async def get_tkr(self, ctx: Context, nickname: str = ""):
        message = await ctx.send(embed=LOADING_EMBED)

        if not nickname:
            nickname = ctx.message.author.name
        nickname = nickname.lower()

        client = hypixel.Client(API_KEY)
        async with client:
            try:
                player = await client.player(nickname)
            except HypixelException:
                embed = Embed(
                    title=ERROR_MESSAGE,
                    description=NO_SUCH_PLAYER_MESSAGE,
                    color=ERROR_COLOR,
                )
                embed.set_footer(text=f"Использование — {COMMAND_PREFIX}tkr <никнейм>")
                await message.edit(embed=embed)
                return

        player_uuid = player.uuid

        player_rank_title = player.rank
        if player_rank_title:
            player_rank_title = f"[{player.rank}]"
        else:
            player_rank_title = ""

        embed = Embed(
            title=f"{player_rank_title} {player.name}",
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
                f"H/R: {format_number(player.tkr.br)}\n"
                f"\n"
                f"Удары синей торпедой: {format_number(player.tkr.blue_torpedo_hits)}\n"
                f"\n"
                f"Монеты: {format_number(player.tkr.coins)}"
            ),
            color=SUCCESS_COLOR,
        )

        embed.set_thumbnail(url=create_head(player_uuid))
        embed.set_footer(text=HELP_FOOTER)
        embed.set_author(
            name=f"Turbo Kart Racers статистика {player.name}",
            icon_url=create_avatar(player_uuid),
        )

        await message.edit(embed=embed)

    @commands.command(name="paintball")
    async def get_paintball(self, ctx: Context, nickname: str = ""):
        message = await ctx.send(embed=LOADING_EMBED)

        if not nickname:
            nickname = ctx.message.author.name
        nickname = nickname.lower()

        client = hypixel.Client(API_KEY)
        async with client:
            try:
                player = await client.player(nickname)
            except HypixelException:
                embed = Embed(
                    title=ERROR_MESSAGE,
                    description=NO_SUCH_PLAYER_MESSAGE,
                    color=ERROR_COLOR,
                )
                embed.set_footer(
                    text=f"Использование — {COMMAND_PREFIX}paintball <никнейм>"
                )
                await message.edit(embed=embed)
                return

        player_uuid = player.uuid

        player_rank_title = player.rank
        if player_rank_title:
            player_rank_title = f"[{player.rank}]"
        else:
            player_rank_title = ""

        embed = Embed(
            title=f"{player_rank_title} {player.name}",
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
        embed.set_footer(text=HELP_FOOTER)
        embed.set_author(
            name=f"Paintball статистика {player.name}",
            icon_url=create_avatar(player_uuid),
        )

        await message.edit(embed=embed)
