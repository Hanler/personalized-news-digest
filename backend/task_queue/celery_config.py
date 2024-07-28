from celery import Celery
from config.settings import BROKER_URL, RESULT_BACKEND


app = Celery('tasks', broker=BROKER_URL, backend=RESULT_BACKEND)
