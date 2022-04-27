import math

import requests


def format_number(number):
    return "{:,}".format(number).replace(",", " ")


def format_date(date):
    return date.strftime("%d.%m.%Y %H:%M")


def round_number(number):
    return round(number, 2)


def floor_number(number):
    return math.floor(number)


def create_head(uuid):
    return f"https://crafatar.com/renders/head/{uuid}?overlay"


def create_skin(uuid):
    return f"https://crafatar.com/renders/body/{uuid}?overlay"


def create_avatar(uuid):
    return f"https://crafatar.com/avatars/{uuid}?overlay"


def get_player_by_uuid(uuid):
    request = requests.get(
        "https://api.mojang.com/user/profiles/%s/names" % uuid
    ).json()
    username = request[-1].get("name")
    return username
