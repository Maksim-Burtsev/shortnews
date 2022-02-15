import requests
from bs4 import BeautifulSoup
import json
import sqlite3
import datetime
import os

N = 1

URLS = [
    f'https://habr.com/ru/search/page{i}/?q=Python&target_type=posts&order=date' for i in range(1, 6)]


def make_json():
    """Парсит данные каждой страницы и делает из них json"""

    data_dict = {}

    for page in range(len(URLS)):
        data_dict[page] = parser(URLS[page])

    with open('habr.json', 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, indent=4, ensure_ascii=False)


def parser(url: str):
    """Парсит одну страницу и возвращает результат в виде словаря"""

    global N

    res_dict = {}

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    div = soup.find('div', {'class': 'tm-articles-list'})
    links = div.find_all('a', {'class': 'tm-article-snippet__title-link'})

    for i in range(len(links)):
        res_dict[N] = {
            'title': links[i].text,
            'link': 'https://habr.com' + links[i].get('href')}

        N += 1

    return res_dict


def get_data():
    """Распаковывает json и формирует из него готовые tuple для записи в базу данных"""

    with open('habr.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    post_num = 1
    articles = []
    news_id = 1

    for i in range(5):
        for j in range(20):
            try:
                articles.append(
                    (data[str(i)][str(post_num)]['title'], data[str(i)][str(post_num)]['link'], datetime.datetime.now(), news_id))
            except:
                articles.append(('oops', '#', datetime.datetime.now(), news_id))
                
            post_num += 1
            news_id += 1

    return articles


def update_database():
    """Обновляет базу данных"""

    try:
        sqlite_connection = sqlite3.connect(
            "C:\\Users\\user\\h_w\\shortnews\\db.sqlite3")
    except:
        sqlite_connection = sqlite3.connect("E:\shortnews\shortnews\db.sqlite3")

    cursor = sqlite_connection.cursor()

    sql_update_query = """Update news_news set title = ?, link = ?, time_created = ? where id = ?"""

    articles = get_data()
    cursor.executemany(sql_update_query, articles)

    sqlite_connection.commit()
    cursor.close()

    sqlite_connection.close()

    os.remove('habr.json')


def habr_main():
    make_json()
    update_database()


if __name__ == '__main__':
    habr_main()
