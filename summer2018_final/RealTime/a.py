import pika

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
        self.connection.publish(
            exchange=EXCHANGE_NAME,
            routing_key='raw',
            body=raw)
