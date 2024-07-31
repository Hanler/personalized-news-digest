from task_queue.tasks import link_scraper_task
from config.settings import SITES_STACK

def launch_link_scrapers(links):
    """
    Launch the LinkScraper instances
    with links from the pre-defined stack
    """
    for link in links:
        link_scraper_task.apply_async(args=[link], queue='link_scraper')

def main():
    # producer = LinkScraper(link="https://www.bbc.com/")
    launch_link_scrapers(SITES_STACK)

if __name__ == '__main__':
    main()
