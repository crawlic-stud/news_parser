import json
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup


MONTHS = ["", "янв", "фев", "мар", "апр", "мая", "июн", "июл", "авг", "сент", "окт", "нояб", "дек"]


def get_news_by_category(page=0, category="politics"):
    """Scrapes news from chosen category"""
    if page < 0:
        return []

    url = f"https://www.rbc.ru/v10/ajax/get-news-by-filters/?category={category}&offset={page*12}&limit=12"

    req = requests.get(url)
    data = json.loads(req.text)["html"]

    soup = BeautifulSoup(data, "html.parser")

    titles = soup.find_all("span", class_="item__title")
    titles_text = [title.text.strip() for title in titles]

    date_time = soup.find_all("span", class_="item__category")
    dt_text = [dt.text.strip().split(", ")[::-1] for dt in date_time]

    for i, dt in enumerate(dt_text):
        if len(dt) == 1:
            dt_text[i].append(f"{datetime.now().day} {MONTHS[datetime.now().month]}")

    dates = [dt[1] for dt in dt_text]
    times = [dt[0] for dt in dt_text]

    links = soup.find_all("a", class_="item__link")
    links = [link["href"] for link in links]

    result = [{"title": d[0], "time": d[1], "date": d[2], "link": d[3]}
              for d in zip(titles_text, times, dates, links)]

    return result


def main():
    urls = []
    max_pages = 84

    # how many pages to parse
    for i in range(1):
        urls.append((i, "politics"))
        urls.append((i, "society"))
        urls.append((i, "business"))
        urls.append((i, "economics"))
        urls.append((i, "finances"))
        urls.append((i, "technology_and_media"))
    start = time.perf_counter()
    for url in urls:
        [print(new) for new in get_news_by_category(*url)]
        get_news_by_category(*url)
    print(time.perf_counter() - start)


if __name__ == '__main__':
    main()

