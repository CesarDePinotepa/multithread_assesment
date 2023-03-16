import csv
import threading
import time


from typing import List

from utils.network import Network
from service.model.message import Message


class Logging(threading.Thread):
    """
    A class representing a logger that extends the threading.Thread class to log sensor data in a separate thread.
    """
    def __init__(self, network: Network, file_name: str, data_source: str):
        super().__init__()
        self.network: Network = network
        self.file_name = file_name
        self.data_source = data_source

    def run(self) -> None:
        """
         Continuously receive sensor data from the network and log it to a CSV file.
         """
        while True:
            time.sleep(5)
            data = self.network.receive()
            if self.data_source == ".csv":
                self.log_to_csv(data)
            elif self.data_source == ".txt":
                self.log_to_txt(data)
            else:
                raise ValueError(f"Invalid file type: {self.data_source}")

    def log_to_csv(self, data: List[Message]) -> None:
        """
        Log the given sensor data to a CSV file.

        Parameter:
            data: A list of Message objects to be logged.
        """
        with open(self.file_name, mode='a', newline='') as f:
            writer = csv.writer(f)
            for entry in data:
                row = [entry.timestamp, entry.id, entry.sensor_name, entry.value]
                writer.writerow(row)
                print(f"Logged row to CSV: {row}")

    def log_to_txt(self, data: List[Message]):
        """
        Log the given sensor data to a TXT file and print the logged rows.

        Parameter:
            A list of Message objects to be logged.
        """
        with open(self.file_name, mode='a', newline='') as f:
            for entry in data:
                row = f"{entry.timestamp}, {entry.id}, {entry.sensor_name}, {entry.value}\n"
                f.write(row)
                print(f"Logged row to TXT: {row.strip()}")
