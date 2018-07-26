#! /usr/lib/python3

import numpy as np
import sys
from scipy.fftpack import fft

import os
import pika

import time

EXCHANGE_NAME = 'radar'

class rmq_commumication():
    def __init__(self):
        self.connection = self.get_connection()
        self.in_queue = self.subscribe(self.connection)

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


    def subscribe(self, channel):
        result = channel.queue_declare(exclusive=True)
        in_queue = result.method.queue
        channel.queue_bind(
            queue=in_queue,
            exchange=EXCHANGE_NAME,
            routing_key='max'
        )
        return in_queue

    # TODO
    def publish(self, result_time, result_data):
        data = result_time.tostring() + result_data.tostring()
        headers = {'result_time': len(result_time.tostring()), 'result': len(result_data.tostring())}
        pika_properties = pika.BasicProperties(headers=headers)
        # pika_properties = pika.BasicProperties(content_type='application/json', headers=headers)
        self.connection.publish(
            exchange=EXCHANGE_NAME,
            properties=pika_properties,
            routing_key='kalman',
            body=data)


    def get(self):
        method, properties, body = self.connection.basic_get(queue=self.in_queue, no_ack=True)

        if method is None:
            return None, None

        headers = properties.headers

        if len(body) != 0:
            self.max_time = np.fromstring(np.array(body[:headers['max_data']]), dtype=np.float64)
            self.max_data = np.fromstring(np.array(body[headers['max_data']:]), dtype=np.float64)
        else:
            return None, None
        # print(self.sync.shape, self.sync, self.data)
        return self.max_time, self.max_data


if __name__ == '__main__':
    print('Connect RMQ')
    rabbitmq = rmq_commumication()

    try:
        while(True):
            max_time, max_data = rabbitmq.get()
            if max_time is None:
                time.sleep(0.2)
                continue

            st = time.time() * 1000

            print(max_time)
            print(max_data)

            et = time.time()*1000

            # rabbitmq.publish(max_data)


    except(KeyboardInterrupt, Exception) as ex:
        print(ex)
    finally:
        print('Close all')
        rabbitmq.connection.close()