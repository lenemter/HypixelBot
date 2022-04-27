import re

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
}
HYPIXEL_URL = "https://hypixel.net"
LINK_REGEX = re.compile("^\/threads\/")


def get_news(count: int = 10):
    """Парсит hypixel.net и возвращает ссылки на новости"""
    result_links = []

    current_page = 1
    while True:
        request = requests.get(
            HYPIXEL_URL, headers=HEADERS, params={"page": current_page}
        )
        page = request.text
        current_page += 1

        all_page_soup = BeautifulSoup(page, "html.parser")
        news_div = all_page_soup.find("div", class_="p-body-pageContent")
        news_div_soup = BeautifulSoup(str(news_div), "html.parser")
        news_a = news_div_soup.findAll("a", {"href": LINK_REGEX})

        if not news_a:
            break

        for a in news_a:
            link = a["href"].rstrip("unread")
            link = f"{HYPIXEL_URL}{link}"
            if link in result_links:
                continue
            result_links.append(link)

            if len(result_links) == count:
                return result_links

    return result_links
