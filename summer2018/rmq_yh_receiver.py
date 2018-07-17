#! /usr/lib/python3

import time
import argparse

from serial import Serial, SerialException

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


def publish(channel, message):
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key='raw',
        body=message
    )


def main(args):
    try:
        data = bytearray()
        sender = get_connection()
        start_time = time.time()
        print('begin receiving...')
        with Serial(args.device, 115200) as serial:
            while True:
                if serial.inWaiting() > 0:
                    data.extend(serial.read(serial.inWaiting()))
                else:
                    time.sleep(0.01)
                current_time = time.time()
                if current_time - start_time > 1.0:
                    publish(sender, data)
                    data = bytearray()
                    start_time = current_time
    except (KeyboardInterrupt, Exception) as ex:
        print(ex)
    finally:
        sender.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--device', dest='device', help='Device path')

    main(parser.parse_args())
