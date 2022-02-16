import requests
from bs4 import BeautifulSoup
import datetime
import sqlite3


def parser() -> list:
    """Парсит страницу и возвращает список заголовков и ссылок на статью"""

    URL = 'https://www.nytimes.com/section/technology'

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'lxml')

    section = soup.find('section', {'id': 'stream-panel'})

    li = section.find_all('li', {'class': 'css-ye6x8s'})

    res = []

    for i in range(len(li)):
        link = 'https://www.nytimes.com/' + li[i].find('a').get('href')
        title = li[i].find('h2').text

        res.append((title, link))

    return res

def pack_data(data: list):
    """Формирует список кортежей для записи в базу данных"""
    
    clean_data = []
    db_id = 101

    for article in data:
        clean_data.append((article[0], article[1], datetime.datetime.now(), db_id))

        db_id += 1

    return clean_data

def update_db(data):
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


def nyt_tech_main():
    data = parser()
    
    clean_data = pack_data(data)

    update_db(clean_data)

if __name__ == '__main__':
    nyt_tech_main()
