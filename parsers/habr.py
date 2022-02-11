import requests
from bs4 import BeautifulSoup
import json
import sqlite3
import datetime
import os

N = 1 #����� ����

URLS = [
    f'https://habr.com/ru/search/page{i}/?q=Python&target_type=posts&order=date' for i in range(1, 6)] #urls ��� ��࠭�� �� ������ Python 


def make_json():

    data_dict = {}

    for page in range(len(URLS)):
        data_dict[page] = parser(URLS[page])

    with open('habr.json', 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, indent=4, ensure_ascii=False)


def parser(url: str):

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

    with open('habr.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    post_num = 1
    articles = []
    news_id = 1

    for i in range(5):
        for j in range(20):
            articles.append(
                (news_id, data[str(i)][str(post_num)]['title'], data[str(i)][str(post_num)]['link'], True, datetime.datetime.now(), 1))
            post_num += 1
            news_id += 1

    return articles


def update_database():

    # conn = sqlite3.connect("E:\shortnews\shortnews\db.sqlite3")
    conn = sqlite3.connect("C:\\Users\\user\\h_w\\shortnews\\db.sqlite3")
    cursor = conn.cursor()

    articles = get_data()  # ᯨ᮪ tuple
    cursor.executemany("INSERT INTO news_news VALUES (?,?,?,?,?,?)", articles)
    conn.commit()
    os.remove('habr.json')


if __name__ == '__main__':
    make_json()
    update_database()

