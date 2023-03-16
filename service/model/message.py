
from dataclasses import dataclass


@dataclass
class Message:
    """
    A dataclass representing sensor data with a timestamp, unique ID, sensor name, and value.
    """
    timestamp: float
    id: str
    sensor_name: str
    value: int
