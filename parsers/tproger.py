import requests
from bs4 import BeautifulSoup
from funcs import clean_data, update_database

URL = 'https://tproger.ru/'


def parse(page_num: int):
    """Парсит веб-страницу и возвращает с неё все заголовки и ссылки в виде списков"""

    url = URL + f"page/{page_num}/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    div = soup.find('div', {'class': 'main__posts-wrapper'})

    a = div.find_all('a', {'class': 'article__link'})
    title = []
    link = []

    for i in a:
        title.append(i.text)
        link.append(i.get('href'))

    return title, link


def main():
    titles, links = [], []

    for i in range(1, 2):
        title, link = parse(i)

        titles.extend(title)
        links.extend(link)

    data = clean_data(titles, links, 111)
    update_database(data)


if __name__ == '__main__':
    main()
