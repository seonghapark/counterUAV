#! /usr/lib/python3

from test_sort_fft_draw import *

import time
import argparse

import pika

EXCHANGE_NAME = 'radar'


def get_connection(url='amqp://localhost'):
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


def send(channel, message):
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key='raw',
        body=message
    )


def main():
    try:
        sender = get_connection()
        data = bytearray()
        data.append(0x00)
        data.append(0x01)
        data.append(0x02)
        data.append(0x03)
        print('data', data)
        while(True):
            send(sender, data)

    except(KeyboardInterrupt, Exception) as ex:
        print(ex)
    finally:
        sender.close()

if __name__ == '__main__':
    main()
