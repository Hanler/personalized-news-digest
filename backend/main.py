import threading
from scrapers.ArticleScraper import ArticleScraper
from scrapers.LinkScraper import LinkScraper


def producer_task(producer, tasks):
    for task in tasks:
        producer.send_task(task)

def main_multithreading():
    # Create instances of ArticleScraper (producers)
    producers = [ArticleScraper() for _ in range(5)]

    # List of tasks to be processed
    tasks = [f"Article {i}" for i in range(10)]

    # Create and start threads for each producer
    threads = []
    for producer in producers:
        thread = threading.Thread(target=producer_task, args=(producer, tasks))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

def main():
    producer = LinkScraper(link="https://www.bbc.com/")
    # producer = ArticleScraper(link="https://www.bbc.com/")

if __name__ == '__main__':
    main()
