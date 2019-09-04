#! /usr/bin/python3
import sys
from scipy.io import wavfile
import os

from serial import Serial, SerialException
import argparse
import pika

import time
import numpy as np

import struct

EXCHANGE_NAME = 'radar'


class rmq_commumication():
    def __init__(self):
        self.leftarray = []
        self.rightarray = []
        self.sync = []
        self.thresh = 0  # Threshold for Sync is 0 Voltage
        self.msB = 0
        self.lsB = 0

        self.connection = self.get_connection()

    def get_connection(self, url='amqp://localhost'):
        parameters = pika.URLParameters(url)

        parameters.connection_attempts = 5
        parameters.retry_delay = 5.0
        parameters.socket_timeout = 2.0
        connection = pika.BlockingConnection(parameters)

        channel = connection.channel()

        channel.exchange_declare(
            EXCHANGE_NAME,
            exchange_type='direct',
            durable=True
        )
        return channel


    def publish(self, raw):
        print("PUBLISH")
        self.connection.publish(
            exchange=EXCHANGE_NAME,
            routing_key='raw',
            body=raw)

    def publish_write(self, raw):
        print("PUBLISH")
        self.connection.publish(
            exchange=EXCHANGE_NAME,
            routing_key='write',
            body=raw)


def main(args):
    # binary_data = open('/home/cuav/repo/counterUAV/summer2018_final/RealTime/raw_data/raw_recording.txt','wb')   # Create a file
    try:
        data = bytearray()
        rabbitmq = rmq_commumication()
        start_time = time.time()
        print('begin receiving...')
        with Serial(args.device, 115200) as serial:
            while True:
                if serial.inWaiting() > 0:
                    data.extend(serial.read(serial.inWaiting()))
                else:
                    time.sleep(0.01)
                current_time = time.time()
                if current_time - start_time > 1:
                    print(len(data))
                    # if len(data) >= 11025:
                    #     rabbitmq.publish(data[:11025])
                    if len(data) >= 11724:
                        rabbitmq.publish(data[:11724])
                        rabbitmq.publish_write(data[:11724])

                    # lengthMSb = bytes([11025 >> 8])
                    # lengthLSb = bytes([11025 & 0xFF])
                    # binary_data.write(lengthMSb + lengthLSb + data)

                    data = bytearray()
                    start_time = current_time
    except (KeyboardInterrupt, Exception) as ex:
        print(ex)
    finally:
        rabbitmq.connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--device', dest='device', help='Device path')

    main(parser.parse_args())
