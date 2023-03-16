
import threading

from collections import deque
from typing import Dict, List, Tuple
from service.model.message import Message


class Network:
    """
     A class that simulates the network for sending and receiving sensor data with a limited queue.
     """

    def __init__(self, max_messages: int = 5):
        self.queue = deque(maxlen=max_messages)
        self.semaphore = threading.Semaphore(max_messages)

    def send(self, data: Message) -> bool:
        """
        Send sensor data to the network queue. If the semaphore is available, append the data and return True.
        Otherwise, return False.

        :param data: SensorData object to be sent.
        :return: True if data is sent successfully, False otherwise.
        """
        if self.semaphore.acquire(blocking=False):
            self.queue.append(data)
            return True
        return False

    def release(self):
        """
        Release the semaphore when a message is removed from the queue.
        """
        self.semaphore.release()

    def receive(self) -> List[Message]:
        """
        Receive all sensor data in the network queue, release the semaphore for each removed message, and clear the queue.

        :return: A list of SensorData objects.
        """
        data = list(self.queue)
        for _ in self.queue:
            self.release()
        self.queue.clear()
        return data

