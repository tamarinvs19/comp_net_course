from threading import Thread
from typing import Callable
from queue import Queue

from config import Task


class ThreadPool:
    def __init__(self, num_threads: int, handler: Callable):
        self.num_threads = num_threads
        self.queue: Queue[Task] = Queue(num_threads)
        self.is_active = False
        self.handler = handler
        self.threads = [
            Thread(target=self.run_handler)
            for _ in range(num_threads)
        ]

    def run_handler(self):
        while self.is_active:
            task = self.queue.get(block=True)
            self.handler(task)
            self.queue.task_done()

    def start(self):
        self.is_active = True
        for thread in self.threads:
            thread.start()

    def join(self):
        self.queue.join()
        self.is_active = False
        for thread in self.threads:
            thread.join()

    def push(self, task: Task):
        self.queue.put(task)
