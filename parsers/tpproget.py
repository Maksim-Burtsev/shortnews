import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime

URL = 'https://tproger.ru/'


def parse(page_num: int):
    """Парсит веб-страницу и возвращает с неё все заголовки и ссылки в виде списков"""

    url = URL + f"page/{page_num}/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    div = soup.find('div', {'class': 'main__posts-wrapper'})

    a = div.find_all('a', {'class': 'article__link'})
    title = []
    link = []

    for i in a:
        title.append(i.text)
        link.append(i.get('href'))

    return title, link


def clean_data(titles: list, links: list):
    """Получает на вход списки названия и ссылок статей и формирует готовые кортежи для записи в БД"""
    post_id = 111
    is_published = True
    time_created = datetime.datetime.now()
    cat_id = 3

    res = []

    for i in range(len(titles)):
        tmp = (post_id, titles[i], links[i],
               is_published, time_created, cat_id)
        post_id += 1
        res.append(tmp)

    return res


def update_database(titles: list, links: list):
    """Записывает в базу данных"""
    conn = sqlite3.connect("C:\\Users\\user\\h_w\\shortnews\\db.sqlite3")
    cursor = conn.cursor()

    articles = clean_data(titles, links)  # ᯨ᮪ tuple
    cursor.executemany("INSERT INTO news_news VALUES (?,?,?,?,?,?)", articles)
    conn.commit()


def main():
    titles, links = [], []

    for i in range(1, 6):
        title, link = parse(i)

        titles.extend(title)
        links.extend(link)

    update_database(titles, links)


if __name__ == '__main__':
    main()
