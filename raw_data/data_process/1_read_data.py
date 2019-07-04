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
        # raw needs (name, index, length, data)
        headers = {
            'name': raw['name'],
            'index': raw['index'],
            'length': raw['length']
        }
        pika_properties = pika.BasicProperties(headers=headers)
        self.connection.publish(
            exchange=EXCHANGE_NAME,
            properties=pika_properties,
            routing_key='raw',
            body=raw['data'])


if __name__ == '__main__':

    # read file
    pwd = os.getcwd()# current working folder
    # file_name = pwd+ '/' +sys.argv[1]
    file_name = sys.argv[1]
    file = open(file_name, "rb")
    read_data = file.read()

    data = bytearray()
    print('Connect RMQ')
    rabbitmq = rmq_commumication()

    try:
        # divide input
        print(len(read_data)//11724)
        for i in range(int(len(read_data)//11724)):
            print(i)
            # publish raw data with header
            raw = {
                'name': sys.argv[1],
                'index': i,
                'length': int(len(read_data)//11724),                
                'data': read_data[i*11724:(i+1)*11724]
            }
            rabbitmq.publish(raw)
            time.sleep(0.1)

    except (KeyboardInterrupt, Exception) as ex:
        print(ex)
    finally:
        print('Close all')
        rabbitmq.connection.close()
        file.close()
