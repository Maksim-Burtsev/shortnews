import os
import requests
from bs4 import BeautifulSoup
import json
import datetime
import sqlite3

URL = 'https://www.nytimes.com/section/technology'

def parser():
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
    with open ('nyt_tech.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=3, ensure_ascii=False)

def get_data():

    with open('nyt_tech.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    
    articles = []
    news_id = 101

    for i in range(10):
        articles.append(
            (news_id, data[str(i)]['title'], data[str(i)]['link'], True, datetime.datetime.now(), 2))
        
        news_id += 1

    return articles

def update_database():

    conn = sqlite3.connect("C:\\Users\\user\\h_w\\shortnews\\db.sqlite3")
    cursor = conn.cursor()

    articles = get_data()  # ᯨ᮪ tuple
    cursor.executemany("INSERT INTO news_news VALUES (?,?,?,?,?,?)", articles)
    conn.commit()
    os.remove('nyt_tech.json')

def main():
    data = parser()
    make_json(data)
    update_database()

if __name__ == '__main__':
    main()