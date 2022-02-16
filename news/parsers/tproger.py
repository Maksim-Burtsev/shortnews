import requests
from bs4 import BeautifulSoup
import datetime
import sqlite3

URL = 'https://tproger.ru/'


def clean_data(titles: list, links: list, post_id: int) -> list:
    """Получает на вход списки названия и ссылок статей и формирует готовые кортежи для записи в БД"""
    time_created = datetime.datetime.now()

    res = []

    for i in range(len(titles)):
        tmp = (titles[i], links[i],
               time_created, post_id)
        post_id += 1
        res.append(tmp)

    return res

def update_database(data: list[tuple]):
    """Обновляет базу данных"""

    try:
        sqlite_connection = sqlite3.connect(
            "C:\\Users\\user\\h_w\\shortnews\\db.sqlite3")
    except:
        sqlite_connection = sqlite3.connect("E:\shortnews\shortnews\db.sqlite3")

    cursor = sqlite_connection.cursor()

    sql_update_query = """Update news_news set title = ?, link = ?, time_created = ? where id = ?"""
    cursor.executemany(sql_update_query, data)

    sqlite_connection.commit()
    cursor.close()

    sqlite_connection.close()

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


def tproger_main():
    titles, links = [], []

    for i in range(1, 2):
        title, link = parse(i)

        titles.extend(title)
        links.extend(link)

    data = clean_data(titles, links, 111)
    update_database(data)


if __name__ == '__main__':
    tproger_main()
