from email.header import Header
import requests
from bs4 import BeautifulSoup
import fake_useragent

user = fake_useragent.UserAgent().random
HEADER = {'user-agent': user}

EURO_URL = 'https://www.banki.ru/products/currency/eur/'
DOLLAR_URL = 'https://www.banki.ru/products/currency/usd/'
BITCOIN_URL = 'https://www.google.com/finance/quote/BTC-USD?sa=X&ved=2ahUKEwjSiZzk6Pz1AhUzQ_EDHUfoDPMQ-fUHegQIDRAS'


def get_euro__dollar_price(url):
    """Получает текущий курс доллара или евро, в зависимости от переданного url.Эти валюты парсятся с одного сайта, поэтому они имеют одинаковые функции."""

    response = requests.get(url, headers=HEADER)
    soup = BeautifulSoup(response.text, 'lxml')

    price = soup.find('div', {'class': 'currency-table__large-text'}).text

    return price


def get_bitcoin_price():
    """Возвращает текущую стоимость биткойна"""

    response = requests.get(BITCOIN_URL, headers=HEADER)
    soup = BeautifulSoup(response.text, 'lxml')

    price = soup.find('div', {'class': 'YMlKec fxKbKc'}).text

    return price


if __name__ == "__main__":
    
    print(f'Биткоин : {get_bitcoin_price()}')
    print(f'Доллар : {get_euro__dollar_price(DOLLAR_URL)}')
    print(f'Евро : {get_euro__dollar_price(EURO_URL)}')