import requests
from bs4 import BeautifulSoup
from funcs import clean_data, update_database

URL = 'https://habr.com/ru/all/'


def parse(url: str):
    """Парсит со страницы все названия статей и ссылки на них"""

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    div = soup.find('div', {'class': 'tm-articles-list'})

    articles = div.find_all('article', {'class': 'tm-articles-list__item'})

    titles = []
    links = []

    for article in articles:
        a = article.find('a', {'class': 'tm-article-snippet__title-link'})
        titles.append(a.text)
        links.append('https://habr.com' + a.get('href'))

    return titles, links


def main():
    titles, links = [], []

    for i in range(1, 6):
        url = URL + f'page{i}/'
        title, link = parse(url)

        titles.extend(title)
        links.extend(link)

    data = clean_data(titles, links, 131)
    update_database(data)


if __name__ == '__main__':
    main()
