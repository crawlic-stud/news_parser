import datetime
import json

import requests
from bs4 import BeautifulSoup
from markovify import NewlineText, Text


def get_main_news_by_date(year, month, day):
    article_url = f"https://web.archive.org/web/{year + month + day}045319/https://www.rbc.ru/politics/{day}/{month}/{year}/62074b119a7947b0e49b36f7"
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, "html.parser")

    article_special = soup.find("div", class_="article__special_container")
    article_special_title = article_special.find("p").text
    article_special_news = [news for news in article_special.find_all("li")]

    special_news_with_links = []
    for new in article_special_news:
        special_news_with_links.append({"text": new.text.strip(),
                                        "link": ""})
        if new.find("a"):
            special_news_with_links[-1]["link"] = new.find("a").get("href")

    return article_url, article_special_title, special_news_with_links


def format_number(num):
    return str(num).zfill(2)


def get_all_dates(year=2022, month=2, day=24):
    curr_date = datetime.datetime.today()
    date_list = [(str(curr_date.year), format_number(curr_date.month), format_number(curr_date.day))]
    while curr_date.year != year:
        curr_date = curr_date - datetime.timedelta(days=1)
        date_list.append((str(curr_date.year), format_number(curr_date.month), format_number(curr_date.day)))
    while curr_date.month != month:
        curr_date = curr_date - datetime.timedelta(days=1)
        date_list.append((str(curr_date.year), format_number(curr_date.month), format_number(curr_date.day)))
    while curr_date.day != day:
        curr_date = curr_date - datetime.timedelta(days=1)
        date_list.append((str(curr_date.year), format_number(curr_date.month), format_number(curr_date.day)))
    return date_list


def collect_all_data_to_json():
    dates = get_all_dates()[::-1]
    all_news_list = []

    for date in dates:
        try:
            print(date, "done")
            url, title, news_list = get_main_news_by_date(*date)
        except Exception as e:
            print(date, f"error: {e}")
            url, title, news_list = "", "", []

        news_dict = {
            "date": ".".join(list(date)),
            "title": title,
            "url": url,
            "news": news_list
        }

        all_news_list.append(news_dict)

    # print(all_news_list)
    # print(json.dumps(all_news_list, indent=4, ensure_ascii=False))
    with open("data.json", "w") as f:
        json.dump(all_news_list, f, ensure_ascii=True, indent=4)


def extract_news_to_txt():
    with open("scraped_data.json", "r") as f:
        data = json.load(f)

    text_data = []
    for each in data:
        news = each["news"]
        for new in news:
            text_data.append(new["text"]) if new["text"] else None

    text_data = "\n".join(text_data)

    with open("text_data.txt", "w", encoding="utf-8") as f:
        f.write(text_data)


def generate_sentence():
    with open("text_data.txt", "r", encoding="utf-8") as f:
        text = f.read()

    # print(text)
    text_model = NewlineText(text, state_size=1, well_formed=True)
    sentence = text_model.make_sentence()
    return sentence


if __name__ == '__main__':
    # print(get_all_dates())
    # collect_all_data_to_json()
    # extract_news_to_txt()
    for _ in range(5):
        print(generate_sentence())
