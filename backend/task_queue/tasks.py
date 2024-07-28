from task_queue.celery_config import app
from nn_worker.NNWorker import NNWorker


# This will store the NNWorker instance
worker_instance = None

@app.task
def process_task(task):
    global worker_instance
    if worker_instance is None:
        worker_instance = NNWorker()
    worker_instance.start(task)
