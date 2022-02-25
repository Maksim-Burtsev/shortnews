from news.parsers.activate import update_db

def make_update():
    """Вызывает функцию обновления БД и после успешного обновления выводит сообщение в консоль"""

    update_db()
    print("База данных обновлена :)")

