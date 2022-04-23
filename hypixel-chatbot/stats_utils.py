import requests
from PIL import Image


def format_number(number):
    return "{:,}".format(number).replace(",", " ")


def format_date(date):
    return date.strftime("%d.%m.%Y %H:%M")


def round_number(number):
    return round(number, 2)


def create_head(uuid):
    return f"https://crafatar.com/renders/head/{uuid}?overlay"
