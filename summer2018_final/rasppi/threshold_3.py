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
        self.max_data = []
        self.max_time = []

    def sorting(self, result_time, result_data):
        self.max_data = []
        self.max_time = []
        for i in range(len(result_data)):   # must 50
            thr_data = []
            for j in range(3, len(result_data[i])//5):    # 220 (44=17m)       # TODO threshold for y
                if result_data[i][j] > -10:  # TODO threshold for amplitude
                    thr_data.append(j)

            # get the mean(average) of distance(j)
            if len(thr_data) != 0:
                thr_data = np.array(thr_data)
                mean = thr_data.mean()
                temp = 3E8/(2*(2500E6-2400E6))*int(5512/50)/2   # TODO
                mean = temp / 220 * mean
                self.max_data.append(mean)
                self.max_time.append(result_time[i])

        return self.max_time, self.max_data

    def sort_max(self, r_time, r_data):
        for i in range(len(r_data)):
            max_value = r_data[i].max()
            indices = np.where(r_data == r_data.max())

            self.max_data.append(max_value)
            print(max_value, indices)
        print(max_data)

        return self.max_data

 

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

        print(len(result_time), len(result_data))

        max_time, max_data = thresh.sorting(result_time, result_data)
        print("max_time: ", max_time, "max_time_length: ", len(max_time), "max_data: ", max_data, "max_data_length: ", len(max_data))
        max_data = thresh.sort_max(result_time, result_data)
        print("max_data_length: ", len(max_data))

        # # extract data based on threshold
        # print("threshold")
        # for i in range(len(result_data)):   # 44 or 46
        #     thr_data = []
        #     for j in range(3, len(result_data[i])//5):    # 220 (44=17m)       # TODO threshold for y
        #         if result_data[i][j] > -20:  # TODO threshold for amplitude
        #             print("yes")
        #             thr_data.append(j)

        #     # get the mean(average) of distance(j)
        #     if len(thr_data) != 0:
        #         thr_data = np.array(thr_data)
        #         mean = thr_data.mean()
        #         temp = 3E8/(2*(2500E6-2400E6))*int(5512/50)/2   # TODO
        #         mean = temp / 220 * mean
        #         max_data.append(mean)
        #         max_time.append(result_time[i])

        rabbitmq.publish(max_time, max_data)


    # except(KeyboardInterrupt, Exception) as ex:
    #     print(ex)
    # finally:
    #     print('Close all')
    #     rabbitmq.connection.close()
