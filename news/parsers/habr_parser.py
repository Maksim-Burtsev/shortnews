import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime
import fake_useragent


URL = 'https://habr.com/ru/all/'


def get_articles_from_page(url) -> list:
    """Парсит все статьи со страницы"""

    user = fake_useragent.UserAgent().random
    header = {
        'user-agent': user,
    }

    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'lxml')

    div = soup.find('div', {'class': 'tm-articles-subpage'})

    articles = div.find_all('article')

    return articles


def get_post_data(article, post_id: int) -> tuple:
    """Достаёт из поста всю необходимую информацию и упаковывает её для записи в БД"""

    try:
        title = article.find(
            'a', {'class': 'tm-article-snippet__title-link'}).text
    except:
        return False

    time = datetime.datetime.strptime(
        article.find('time').get('title'),
        '%Y-%m-%d, %H:%M',
    )

    url = 'https://habr.com' + \
        article.find(
            'a', {'class': 'tm-article-snippet__title-link'}).get('href')

    return (title, url, time, post_id)


def update_database(data: list[tuple]):
    """Обновляет базу данных"""

    try:
        sqlite_connection = sqlite3.connect(
            "E:\shortnews\shortnews\db.sqlite3")
    except:
        sqlite_connection = sqlite3.connect(
            "C:\\Users\\user\\h_w\\shortnews\\db.sqlite3")
    cursor = sqlite_connection.cursor()

    sql_update_query = """Update news_news set title = ?, link = ?, time_created = ? where id = ?"""
    cursor.executemany(sql_update_query, data)

    sqlite_connection.commit()
    cursor.close()

    sqlite_connection.close()


def habr_parser_main():
    """Основная функция программы"""

    URL = 'https://habr.com/ru/all/page'
    all_data = []
    post_id = 131

    for i in range(1, 6):
        url = URL + str(i) + '/'
        articles = get_articles_from_page(url)
        for j in range(len(articles)):
            data = get_post_data(articles[j], post_id)
            if data:
                all_data.append(data)
                post_id += 1
            else:
                pass
            print(f'article{j+1}/{len(articles)}')
        print(f'page {i}/5')

        update_database(all_data)


if __name__ == '__main__':
    habr_parser_main()
