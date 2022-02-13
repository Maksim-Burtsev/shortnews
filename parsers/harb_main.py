import re
import requests
from bs4 import BeautifulSoup
import datetime
import sqlite3

URL = 'https://habr.com/ru/all/'


def parse(url: str):
    """Парсит со страницы все названия статей и ссылки на них"""

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    div = soup.find('div', {'class': 'tm-articles-list'})

    articles = div.find_all('article', {'class': 'tm-articles-list__item'})

    titles = []
    links = []

    for article in articles:
        a = article.find('a', {'class': 'tm-article-snippet__title-link'})
        titles.append(a.text)
        links.append('https://habr.com' + a.get('href'))

    return titles, links


def clean_data(titles: list, links: list):
    """Получает на вход списки названия и ссылок статей и формирует готовые кортежи для записи в БД"""
    post_id = 131
    time_created = datetime.datetime.now()

    res = []

    for i in range(len(titles)):
        tmp = (titles[i], links[i],
               time_created, post_id)
        post_id += 1
        res.append(tmp)

    return res


def update_database(titles: list, links: list):
    """Обноваляет базу данных"""

    sqlite_connection = sqlite3.connect(
        "C:\\Users\\user\\h_w\\shortnews\\db.sqlite3")

    cursor = sqlite_connection.cursor()

    sql_update_query = """Update news_news set title = ?, link = ?, time_created = ? where id = ?"""
    articles = clean_data(titles, links)
    cursor.executemany(sql_update_query, articles)

    sqlite_connection.commit()
    cursor.close()

    sqlite_connection.close()


def main():
    titles, links = [], []

    for i in range(1, 6):
        url = URL + f'page{i}/'
        title, link = parse(url)

        titles.extend(title)
        links.extend(link)

    update_database(titles, links)


if __name__ == '__main__':
    main()
