from apscheduler.schedulers.background import BackgroundScheduler
from .smthng_upd import foo


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(foo, 'interval', seconds=600)
    scheduler.start()