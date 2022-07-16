import math
import time

import requests


def format_number(number):

    """
    Функция для форматирования числа.
    Пример: 1234567 -> 1 234 567.
    """

    return "{:,}".format(number).replace(",", " ")


def format_date(date):

    """
    Функция для форматирования даты.
    Пример: 2014-05-02 23:23:10.734000+00:00 -> 02.05.2014 23:23.
    """

    return date.strftime("%d.%m.%Y %H:%M")


def round_number(number):

    """
    Функция для округления числа.
    Пример: 123.456789 -> 123.46.
    """

    return round(number, 2)


def floor_number(number):

    """
    Функция для округления числа в меньшую сторону.
    Пример: 123.456789 -> 123.
    """

    return math.floor(number)


def create_head(uuid):

    """
    Функция для создания рендера головы скина игрока.
    """

    return f"https://crafatar.com/renders/head/{uuid}?overlay?{time.time()}"


def create_skin(uuid):

    """
    Функция для создания рендера скины игрока.
    """

    return f"https://crafatar.com/renders/body/{uuid}?overlay?{time.time()}"


def create_avatar(uuid):

    """
    Функция для создания аватарки игрока.
    """

    return f"https://crafatar.com/avatars/{uuid}?overlay"


def get_player_by_uuid(uuid):

    """
    Фунцкия для получения никнейма игрока по его уникальному идентификатору.
    Пример: ed4c07df-b4d7-4c6e-8bdc-3f5b5e2c0a29 -> namzhil.
    """

    request = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()
    username = request[-1].get("name")
    return username
