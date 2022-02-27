from news.parsers.activate import update_db

import logging


def make_update():
    """Вызывает функцию обновления БД и после успешного обновления выводит  сообщение в консоль"""

    logger = logging.getLogger('news')

    try:
        update_db()
    except Exception as e:
        logger.exception(f'{e} при обновлении базы данных')
    else:
        logger.info('База данных успешно обновлена')
