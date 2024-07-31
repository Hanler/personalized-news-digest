from celery import Celery
from config.settings import BROKER_URL, RESULT_BACKEND


class CeleryConfig:
    broker_url = BROKER_URL
    result_backend = RESULT_BACKEND
    task_queues = {
        'link_scraper': {
            'exchange': 'link_scraper',
            'routing_key': 'link_scraper'
        },
        'article_scraper': {
            'exchange': 'article_scraper',
            'routing_key': 'article_scraper'
        },
        'nn_worker': {
            'exchange': 'nn_worker',
            'routing_key': 'nn_worker'
        }
    }
    task_routes = {
        'tasks.link_scraper_task': {'queue': 'link_scraper'},
        'tasks.article_scraper_task': {'queue': 'article_scraper'},
        'tasks.nn_worker_task': {'queue': 'nn_worker'},
    }

app = Celery('tasks')
app.config_from_object(CeleryConfig)
