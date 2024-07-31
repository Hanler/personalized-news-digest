from celery import Celery
import time


class NNWorker(object):
    """
    A class used to represent a neural network worker that processes articles
    """
    def __init__(self):     
        print("NNWorker was inited")

    def start(self, id, article):
        """
        Run the NN worker
        """
        print(f"Worker gets the task: {article}")
        time.sleep(3)
        print(f"End task {article}")
