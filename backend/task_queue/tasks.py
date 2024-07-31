import os, sys
from task_queue.celery_config import app
from nn_worker.NNWorker import NNWorker

# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# This will store the NNWorker instance
nn_worker_instance = None

@app.task
def link_scraper_task(link):
    from scrapers.LinkScraper import LinkScraper
    print(f"LinkScraper was spawned with {link}")
    link_scraper_instance = LinkScraper(link)

@app.task
def article_scraper_task(id, link):
    from scrapers.ArticleScraper import ArticleScraper 
    print(f"ArticleScraper was spawned with {id} -- {link}")
    article_scraper_instance = ArticleScraper(id, link)

@app.task
def nn_worker_task(id, text):
    global nn_worker_instance
    if nn_worker_instance is None:
        nn_worker_instance = NNWorker()
    nn_worker_instance.start(id, text)
