from queue import Queue
from typing import List


class Notifier:

    def __init__(self):
        self.subscribers: List[Queue] = []

    def subscribe(self):
        queue = Queue()

        self.subscribers.append(queue)

        return self._events_generator(queue)

    def publish(self, data: str):
        for subscriber in self.subscribers:
            subscriber.put(data)

    def _events_generator(self, queue: Queue):
        while True:
            data = queue.get()
            if data is None:
                return
            yield data
