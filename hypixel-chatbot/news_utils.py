from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from time import sleep
from pprint import pprint

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
}
HYPIXEL_URL = "https://hypixel.net"


@dataclass(repr=False)
class News:
    link: str
    title: str
    date: str = ""
    description: str = ""

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.title


def get_news(count: int = 10):
    result_news = []

    current_page = 1
    while True:
        request = requests.get(
            HYPIXEL_URL, headers=HEADERS, params={"page": current_page}
        )
        print(f"{current_page} {request.status_code=}")
        current_page += 1

        soup = BeautifulSoup(request.text, "html.parser")
        div_news = soup.find("div", class_="p-body-pageContent")
        soup = BeautifulSoup(str(div_news), "html.parser")
        all_news = soup.findAll("a", href=True)

        links = set()
        for new in all_news:
            if new["href"].startswith("/threads/"):
                link = f"{HYPIXEL_URL}{new['href']}".rstrip("unread")
                if link in links:
                    continue
                links.add(link)
                title = new.text

                new_new = News(link=link, title=title)
                result_news.append(new_new)

                if len(result_news) == count:
                    return result_news

        if not links:
            break

    return result_news


if __name__ == "__main__":
    pprint(get_news())
