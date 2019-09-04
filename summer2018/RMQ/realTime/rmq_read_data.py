#! /usr/bin/python3
import sys
import os
import pika
import time

EXCHANGE_NAME = 'radar'


class rmq_commumication():
    def __init__(self):
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
        self.connection.publish(
            exchange=EXCHANGE_NAME,
            routing_key='raw',
            body=raw)



if __name__ == '__main__':

    # read file
    pwd = os.getcwd() # current working folder
    # file_name = pwd+ '/' +sys.argv[1]
    file_name = sys.argv[1]
    file = open(file_name, 'rb')
    read_data = file.read()

    data = bytearray()
    # print('Connect RMQ')
    rabbitmq = rmq_commumication()

    try:
        # divide input
        # sample_rate = 11025
        sample_rate = 11724
        for i in range(int(len(read_data)//sample_rate)):
            raw = read_data[i*sample_rate:(i+1)*sample_rate]
            rabbitmq.publish(raw)
            time.sleep(1)

    except (KeyboardInterrupt, Exception) as ex:
        print(ex)
    finally:
        print('Close all')
        rabbitmq.connection.close()
        file.close()
