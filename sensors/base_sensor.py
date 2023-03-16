import random
import time
import uuid
import threading


from utils.network import Network
from service.model.message import Message


class BaseSensor(threading.Thread):
    """
    A class representing a sensor that extends the threading.Thread class to generate sensor data in a separate thread.
    """
    def __init__(self, sensor_name: str,  network: Network, delay: float):
        super().__init__()
        self.sensor_name = sensor_name
        self.network = network
        self.delay = delay

    def run(self) -> None:
        """
        Continuously generate sensor data with a delay and send it to the network.
        """
        while True:
            time.sleep(self.delay)
            data = Message(time.time(), uuid.uuid4().hex, self.sensor_name, random.randint(-100, 100))
            while not self.network.send(data):
                time.sleep(1)


class SensorFactory:
    """
    A factory class for creating sensor objects with different delays.
    """
    @staticmethod
    def create_sensor(sensor_type: str, sensor_name: str, network: Network) -> BaseSensor:
        if sensor_type == "default":
            return BaseSensor(sensor_name, network, 5)
        elif sensor_type == "front_left":
            return BaseSensor(sensor_name, network, 2)
        elif sensor_type == "front_right":
            return BaseSensor(sensor_name, network, 10)
        elif sensor_type == "rear_left":
            return BaseSensor(sensor_name, network, 8)
        elif sensor_type == "rear_right":
            return BaseSensor(sensor_name, network, 9)
        else:
            raise ValueError(f"Invalid sensor type: {sensor_type}")
