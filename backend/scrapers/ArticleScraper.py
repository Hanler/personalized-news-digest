from task_queue.tasks import process_task


class ArticleScraper(object):
    """
    A class used to represent an article scraper that processes
    the page and extracts the article,
    then sends a task for asynchronous processing
    """
    def send_task(self, task):
        """
        Sends a task for asynchronous processing using Celery
        """
        result = process_task.delay(task)
        print(f'Task sent: {task}, Task ID: {result.id}')
