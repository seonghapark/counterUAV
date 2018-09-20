#! /usr/bin/python3
import sys
import os
import pika
import time

import argparse

EXCHANGE_NAME = 'radar'


class rmq_commumication():
    def __init__(self):
        self.connection = self.get_connection()

    # def get_connection(self, url='amqp://localhost'):
    def get_connection(self, url='amqp://192.168.20.83'):
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

    def subscribe(self, channel):
        result = channel.queue_declare(exclusive=True)
        in_queue = result.method.queue
        channel.queue_bind(
            queue=in_queue,
            exchange=EXCHANGE_NAME,
            routing_key='raw'
        )
        return in_queue


    def get(self):
        method, properties, body = self.connection.basic_get(queue=self.in_queue, no_ack=True)

        if method is None:
            return None, None

        data = bytearray(body)

        return data


if __name__ == '__main__':
    print('Connect RMQ') 
    rabbitmq = rmq_commumication()

    timestr = time.strftime("%Y%m%d_%H%M%S")
    file = timestr + '_binary.txt'

    binary_data = open(file,'w+')   # Create a file

    try:
        while(True):
            data = rabbitmq.get()
            if sync is None:
                # print('no incomming data', data)
                time.sleep(0.2)
                continue
            # else:
            #     print('sync: ', sync, ' data: ', data)

            binary_data.write(data)

    except(KeyboardInterrupt, Exception) as ex:
        print(ex)
    finally:
        print('Close all')
        rabbitmq.connection.close()