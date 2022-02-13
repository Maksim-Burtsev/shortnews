import datetime
import sqlite3

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

    sqlite_connection = sqlite3.connect(
        "C:\\Users\\user\\h_w\\shortnews\\db.sqlite3")

    cursor = sqlite_connection.cursor()

    sql_update_query = """Update news_news set title = ?, link = ?, time_created = ? where id = ?"""
    cursor.executemany(sql_update_query, data)

    sqlite_connection.commit()
    cursor.close()

    sqlite_connection.close()