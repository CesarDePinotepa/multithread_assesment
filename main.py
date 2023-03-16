import os
import csv
import argparse


from logging.logging import Logging
from sensors.base_sensor import SensorFactory
from utils.network import Network


def get_parser():
    """
    Get command line parser instance

    Return:
         An instance of the command line parser
    """
    parser = argparse.ArgumentParser(description=__doc__)
    # input
    pgroup = parser.add_argument_group('input')
    pgroup.add_argument('--datasource', metavar='str', default="sensor_data.csv",
                        help='The type of datasource you want to use. It can be csv or txt')

    return parser


def main(file_name: str):
    """Main function"""
    network = Network()

    # create sensors using the factory method
    sensors = [
        SensorFactory.create_sensor("default", "Sensor_Default", network),
        SensorFactory.create_sensor("front_left", "Front_Left", network),
        SensorFactory.create_sensor("front_right", "Front_Right", network),
        SensorFactory.create_sensor("rear_left", "Rear_Left", network),
        SensorFactory.create_sensor("rear_right", "Rear_Right", network),
    ]

    file_extension = os.path.splitext(file_name)[1]
    logger = Logging(network, file_name, data_source=file_extension)

    # write the CSV header
    with open('sensor_data.csv', mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'id', 'sensor_name', 'value'])

    # start the sensor and logger
    for sensor in sensors:
        sensor.start()
    logger.start()


if __name__ == '__main__':
    opts = get_parser().parse_args()
    main(opts.datasource)

