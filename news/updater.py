from apscheduler.schedulers.background import BackgroundScheduler
from news.parser import make_update


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(make_update, 'interval', seconds=600)
    scheduler.start()