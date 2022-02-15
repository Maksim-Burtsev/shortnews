import os
import requests
from bs4 import BeautifulSoup
import json
import datetime
import sqlite3

URL = 'https://www.nytimes.com/section/technology'

def parser():
    """Парсит данные и формирует из них словарь"""
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'lxml')
    
    section = soup.find('section', {'id' : 'stream-panel'})

    li = section.find_all('li', {'class' : 'css-ye6x8s'})
    
    data = {}
    for i in range(len(li)):
        link = 'https://www.nytimes.com/' + li[i].find('a').get('href')
        title = li[i].find('h2').text
        summary = li[i].find('p', {'class' : 'css-1echdzn e15t083i1'}).text

        data[i] = {
            'title' : title,
            'summary' : summary,
            'link' : link,
        }

    return data

def make_json(data: dict):
    """Формирует json из данных после парсинга"""

    with open ('nyt_tech.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=3, ensure_ascii=False)

def get_data():
    """Распаковывает json и формирует из него готовые строки для базы данных"""

    with open('nyt_tech.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    
    articles = []
    news_id = 101

    for i in range(10):
        articles.append(
            (data[str(i)]['title'], data[str(i)]['link'], datetime.datetime.now(), news_id))
        
        news_id += 1

    return articles

def update_database():
    """Обновляет базу данных"""

    sqlite_connection = sqlite3.connect("C:\\Users\\user\\h_w\\shortnews\\db.sqlite3")

    cursor = sqlite_connection.cursor()

    sql_update_query = """Update news_news set title = ?, link = ?, time_created = ? where id = ?"""
    articles = get_data()
    cursor.executemany(sql_update_query, articles)
    
    sqlite_connection.commit()
    cursor.close()

    sqlite_connection.close()

    os.remove('nyt_tech.json')

def nyt_tech_main():
    data = parser()
    make_json(data)
    update_database()

if __name__ == '__main__':
    nyt_tech_main()