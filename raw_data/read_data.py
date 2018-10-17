mport sys
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
    file = open(file_name, "rb")
    read_line = file.readline()

    data = bytearray()
    print('Connect RMQ')
    rabbitmq = rmq_commumication()

    try:
        # divide input
        print(len(read_line)//11025)
        for i in range(int(len(read_line)//11025)):
            raw = read_line[i*11025:(i+1)*11025]
            rabbitmq.publish(raw)
            time.sleep(1)

    except (KeyboardInterrupt, Exception) as ex:
        print(ex)
    finally:
        print('Close all')
        rabbitmq.connection.close()
        file.close()
