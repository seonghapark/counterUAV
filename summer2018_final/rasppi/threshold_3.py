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
            routing_key='ifft'
        )
        return in_queue

    def publish(self, max_time, max_data):
        max_data = np.array(max_data)
        max_time = np.array(max_time)

        data = max_time.tostring() + max_data.tostring()
        headers = {'max_time': len(max_time.tostring()), 'max_data': len(max_data.tostring())}
        pika_properties = pika.BasicProperties(headers=headers)
        # pika_properties = pika.BasicProperties(content_type='application/json', headers=headers)

        self.connection.publish(
            exchange=EXCHANGE_NAME,
            properties=pika_properties,
            routing_key='max',
            body=data)


    def get(self):
        method, properties, body = self.connection.basic_get(queue=self.in_queue, no_ack=True)

        if method is None:
            return None, None

        headers = properties.headers
        self.result_time = np.fromstring(np.array(body[:headers['result_time']]), dtype=np.float64)

        self.result_data = np.fromstring(np.array(body[headers['result_time']:]), dtype=np.float64)
        self.result_data = np.reshape(self.result_data,
                                      (int(len(self.result_time)), int(len(self.result_data) / len(self.result_time))))
        return self.result_time, self.result_data



class sort_by_threshold():
    def __init__(self):
        self.comp_result_data = []
        self.max_idx = []
        self.max_data = []
        self.local_max = 0
        self.idx = 0
        self.local_mean = 0

        self.max_distance = 3E8/(2*(2500E6-2400E6))*int(11724/50)/2

    def sorting(self, result_time, result_data):
        print("in sorting function: ", result_time.shape, result_data.shape)  # (50,), (50, 234) when the sampling rate is 11724

        self.max_data = []
        self.max_idx = []

        for i in range(len(result_data)):   # must 50  # was 44 or 46
            # for j in range(3, len(result_data[i])//5):    # 220 (44=17m)       # TODO threshold for y  # then 250 (50?)
            self.comp_result_data = result_data[i]
            for i in range(5):
                self.local_max = self.comp_result_data.max()
                self.idx = self.comp_result_data.argmax()
                self.max_idx.append(self.idx)

                self.comp_result_data = np.delete(result_data[i], self.idx)

            print(self.max_idx)
            self.max_idx.remove(max(self.max_idx))
            self.local_mean = sum(self.max_idx)/len(self.max_idx)

            distance = self.max_distance / 234 * self.local_mean
            self.max_data.append(distance)
            self.max_idx = []

        self.max_data = np.array(self.max_data)

        return result_time, self.max_data

    def sort_max(self, r_time, r_data):
        print("in sorting function: ", result_time.shape, result_data.shape)  # (50,), (50, 234) when the sampling rate is 11724

        self.max_data = []

        for i in range(len(result_data)):   # must 50  # was 44 or 46
            self.comp_result_data = result_data[i]
            self.idx = self.comp_result_data.argmax()

            # Get distance
            distance = self.max_distance / 234 * self.idx
            self.max_data.append(distance)


        self.max_data = np.array(self.max_data)
        print(self.max_data, len(self.max_data), type(self.max_data), self.max_data[10])

        self.processed_time = []
        for i in range(50):
            temp_time = r_time[i] + 0.0016 * (i + 1)
            self.processed_time.append(temp_time)
        print(r_time[i], self.processed_time)

        return self.processed_time, self.max_data


 

if __name__ == '__main__':
    print('Connect RMQ')
    rabbitmq = rmq_commumication()
    thresh = sort_by_threshold()

    # try:
    while(True):
        result_time, result_data = rabbitmq.get()
        if result_time is None:
            time.sleep(0.2)
            continue

        # max_time, max_data = thresh.sorting(result_time, result_data)
        st = time.time()*1000

        max_time, max_data = thresh.sort_max(result_time, result_data)

        et = time.time()*1000
        print('Sorting elapsed in %2.f' % (et-st))

        rabbitmq.publish(max_time, max_data)


    # except(KeyboardInterrupt, Exception) as ex:
    #     print(ex)
    # finally:
    #     print('Close all')
    #     rabbitmq.connection.close()
