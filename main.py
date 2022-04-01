import json
from datetime import datetime

import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup


MONTHS = ["", "янв", "фев", "мар", "апр", "мая", "июн", "июл", "авг", "сент", "окт", "нояб", "дек"]


def get_trends_titles(page=1):
    """Scrapes trending news titles"""

    url = f"https://trends.rbc.ru/trends/ajax/short_news/?offset={page*12}&limit=8"

    req = requests.get(url)
    data = json.loads(req.text)["html"]

    soup = BeautifulSoup(data, "html.parser")
    titles = soup.find_all("a", class_="item__title")
    titles_text = [title.text.strip() for title in titles]

    if page <= 0:
        titles_text = titles_text[:12]

    return titles_text


def get_news_by_category(page=0, category="politics"):
    """Scrapes news titles from chosen category"""
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

    result = [{"title": d[0], "time": d[1], "date": d[2]} for d in zip(titles_text, times, dates)]

    return result


def check_correct_processing(scraper_func):
    """If nothing is printed then news scraping works correctly."""
    processed = []
    for i in range(100):
        try:
            for t in scraper_func(i):
                if t not in processed:
                    processed.append(t)
                else:
                    print(f"{i=} повторяется")
        except json.decoder.JSONDecodeError:
            print(f"page {i} - no more news")
            break


if __name__ == '__main__':
    # check_correct_processing(get_trends_titles)
    # check_correct_processing(get_news_by_category)
    MAX_AMOUNT = 84
    for i in range(MAX_AMOUNT):
        for new in get_news_by_category(i, category="politics"):
            print(new)

