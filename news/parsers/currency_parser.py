from asyncio.log import logger
import requests
from bs4 import BeautifulSoup
import fake_useragent
import sqlite3
import datetime
import logging

user = fake_useragent.UserAgent().random
HEADER = {'user-agent': user}

EURO_URL = 'https://www.banki.ru/products/currency/eur/'
DOLLAR_URL = 'https://www.banki.ru/products/currency/usd/'
BITCOIN_URL = 'https://www.google.com/finance/quote/BTC-USD?sa=X&ved=2ahUKEwjSiZzk6Pz1AhUzQ_EDHUfoDPMQ-fUHegQIDRAS'


def get_euro__dollar_price(url, val_id, name):
    """Получает текущий курс доллара или евро, в зависимости от переданного url.Эти валюты парсятся с одного сайта, поэтому они имеют одинаковые функции."""

    response = requests.get(url, headers=HEADER)
    soup = BeautifulSoup(response.text, 'lxml')

    price = soup.find('div', {'class': 'currency-table__large-text'}).text

    return (name, float(price.replace(',', '.')), datetime.datetime.now(), val_id)


def get_bitcoin_price():
    """Возвращает текущую стоимость биткойна"""

    response = requests.get(BITCOIN_URL, headers=HEADER)
    soup = BeautifulSoup(response.text, 'lxml')

    price = soup.find('div', {'class': 'YMlKec fxKbKc'}).text
    price = price[:2] + price[3:]
    res = (1, 'bitcoin', float(price.replace(',', '.')), datetime.datetime.now())
    return res


def update_database(data):
    """Обновляет значения валют в БД"""

    try:
        sqlite_connection = sqlite3.connect(
            "C:\\Users\\user\\h_w\\shortnews\\db.sqlite3")
    except:
        sqlite_connection = sqlite3.connect("E:\shortnews\shortnews\db.sqlite3")

    cursor = sqlite_connection.cursor()

    sql_update_query = """Update news_currency set name = ?, price = ?, time_updated = ? where id = ?"""
    cursor.executemany(sql_update_query, data)

    sqlite_connection.commit()
    cursor.close()

    sqlite_connection.close()


def currency_main():

    logger = logging.getLogger('news')

    try:

        data = []
        # data.append(get_bitcoin_price())
        data.append(get_euro__dollar_price(DOLLAR_URL, 1, '$'))
        data.append(get_euro__dollar_price(EURO_URL, 2, '€'))

        update_database(data)

    except Exception as e:
        logger.warning(f'{e} при обновлении курса валют')
    
    else:
        logger.info('Курсы валют успешно обновлены')

if __name__ == "__main__":
    currency_main()
