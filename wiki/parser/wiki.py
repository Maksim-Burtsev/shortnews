import wikipedia
import sqlite3


EXTENSIONS = ('.jpg', 'jpeg', '.png', '.gif')
SKIP_IMAGES = (
    'https://upload.wikimedia.org/wikipedia/commons/b/b4/Red_pog.png',
    'https://upload.wikimedia.org/wikipedia/commons/e/e4/Jupiter_and_moon.png',
    'https://upload.wikimedia.org/wikipedia/commons/6/65/Image-silk.png'
)
wikipedia.set_lang('ru')


def get_image(images: list) -> str:
    """Получает список картинок за страницы и возвращает первую с приемлемым расширением"""

    for image in images:
        if image[-4:] in EXTENSIONS and image not in SKIP_IMAGES:
            return image
    return ''


def get_data(titles: list) -> list[tuple]:
    """Собирает и формирует всю необходимюу информацию о статьях для записи в БД"""
    ID = 1

    res = []
    for title in titles:
        try:
            page = wikipedia.page(title)

        except Exception as e:
            print(e)

        else:
            try:
                summary = page.summary
                url = page.url
                image_link = get_image(page.images)

                res.append((title, summary, url, image_link, ID))

                ID += 1

            except Exception as e:
                print(e)

    return res


def update_db(data):
    """Обновляет базу данных"""

    try:
        sqlite_connection = sqlite3.connect(
            "E:\shortnews\shortnews\db.sqlite3")
    except:
        sqlite_connection = sqlite3.connect(
            "C:\\Users\\user\\h_w\\shortnews\\db.sqlite3")
    cursor = sqlite_connection.cursor()

    sql_update_query = """Update wiki_article set title = ?, summary = ?, url = ?, image_link = ? where id = ?"""
    cursor.executemany(sql_update_query, data)

    sqlite_connection.commit()
    cursor.close()

    sqlite_connection.close()


def update_wiki_db():

    titles = wikipedia.random(pages=45)
    data = get_data(titles)

    update_db(data)

    print(data[0])


if __name__ == '__main__':
    update_wiki_db()
