from turtle import up, update
from news.parsers.habr_parser import habr_parser_main
from news.parsers.habr import habr_main
from news.parsers.currency_parser import currency_main
from news.parsers.tproger import tproger_main
from news.parsers.nyt_tech_parse import nyt_tech_main

def update_db():
    """Запускает основной файл каждого из парсеров, который затем обновляет свои колонки в БД"""
    
    habr_parser_main()
    habr_main()
    currency_main()
    tproger_main()
    nyt_tech_main()

if __name__ == "__main__":
    update_db()