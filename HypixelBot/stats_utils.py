import math
from typing import Optional

import requests

from common import HOST, PORT


def format_number(number) -> str:

    """
    Функция для форматирования числа.
    Пример: 1234567 -> 1 234 567.
    """

    return "{:,}".format(number).replace(",", " ")


def format_date(date) -> str:

    """
    Функция для форматирования даты.
    Пример: 2014-05-02 23:23:10.734000+00:00 -> 02.05.2014 23:23.
    """

    return date.strftime("%d.%m.%Y %H:%M")


def round_number(number) -> float:

    """
    Функция для округления числа.
    Пример: 123.456789 -> 123.46.
    """

    return round(number, 2)


def floor_number(number) -> int:

    """
    Функция для округления числа в меньшую сторону.
    Пример: 123.456789 -> 123.
    """

    return math.floor(number)


def create_head(uuid) -> str:

    """
    Функция для создания рендера головы скина игрока.
    """
    request = requests.get(f"{HOST}:{PORT}/api/head/{uuid}").json()
    return f"{HOST}:{PORT}/{request['url']}"


def create_skin(uuid) -> str:

    """
    Функция для создания рендера скины игрока.
    """
    request = requests.get(f"{HOST}:{PORT}/api/skin/{uuid}").json()
    return f"{HOST}:{PORT}/{request['url']}"


def create_avatar(uuid) -> str:

    """
    Функция для создания аватарки игрока.
    """

    request = requests.get(f"{HOST}:{PORT}/api/avatar/{uuid}").json()
    return f"{HOST}:{PORT}/{request['url']}"


def get_player_by_uuid(uuid) -> Optional[str]:

    """
    Функция для получения никнейма игрока по его уникальному идентификатору.
    Пример: ed4c07df-b4d7-4c6e-8bdc-3f5b5e2c0a29 -> namzhil.
    """

    request = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()
    username = request[-1].get("name")
    return username
