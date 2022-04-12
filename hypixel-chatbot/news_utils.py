from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
}
hypixel_url = "https://hypixel.net"


def get_news():
    page = requests.get(hypixel_url, headers=headers)
    # print(page.status_code)

    filteredNews = []
    allNews = []

    soup = BeautifulSoup(page.text, "html.parser")
    print(soup)
    allNews = soup.findAll(
        "a",
    )
    print(allNews)


if __name__ == "__main__":
    get_news()
