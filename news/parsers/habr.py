import requests
from bs4 import BeautifulSoup
import datetime
import sqlite3

URL = 'https://habr.com/ru/search/page{}/?q=Python&target_type=posts&order=date'


def parser(url) -> list:
    """Парсит веб-страницу и возвращает оттуда все заголовки и ссылки на статьи"""

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    div = soup.find('div', {'class': 'tm-articles-list'})

    articles = div.find_all('article', {'class': 'tm-articles-list__item'})

    res = []

    for article in articles:
        title = article.find(
            'a', {'class': 'tm-article-snippet__title-link'}).text
        link = 'https://habr.com' + \
            article.find(
                'a', {'class': 'tm-article-snippet__title-link'}).get('href')

        res.append((title, link))

    return res


def pack_data(data: list):
    """Формирует готовые кортежи для записи в БД"""
    db_id = 1
    clean_data = []

    for article in data:
        clean_data.append(
            (article[0], article[1], datetime.datetime.now(), db_id))

        db_id += 1

    return clean_data


def update_db(clean_data):
    """Обновляет базу данных
    """

    try:
        sqlite_connection = sqlite3.connect(
            "C:\\Users\\user\\h_w\\shortnews\\db.sqlite3")
    except:
        sqlite_connection = sqlite3.connect(
            "E:\shortnews\shortnews\db.sqlite3")

    cursor = sqlite_connection.cursor()

    sql_update_query = """Update news_news set title = ?, link = ?, time_created = ? where id = ?"""

    cursor.executemany(sql_update_query, clean_data)

    sqlite_connection.commit()
    cursor.close()

    sqlite_connection.close()


def update_habr_python():

    res = []

    for i in range(1, 6):
        res.extend(parser(URL.format(i)))

    data = pack_data(res)

    update_db(data)


if __name__ == '__main__':
    update_habr_python()
