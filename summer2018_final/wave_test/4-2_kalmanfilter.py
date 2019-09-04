#! /usr/lib/python3
import numpy as np
import sys
from scipy.fftpack import fft
import os
import pika
import time

import pylab

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

    def publish(self, max_time, max_data, kalman):
        max_time = np.array(max_time)
        max_data = np.array(max_data)
        kalman = np.array(kalman)
        
        data = max_time.tostring() + max_data.tostring() + kalman.tostring()
        headers = {'max_time': len(max_time.tostring()), 'max_data': len(max_data.tostring()),
                   'kalman_data': len(kalman.tostring())}
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



class kalmanfilter():
    def __init__(self):
        # intial parameters
        self.n_iter = 50
        self.sz = (self.n_iter,) # size of array
        # x = -0.37727 # truth value (typo in example at top of p. 13 calls this z)
        self.x = 0
        # z = np.random.normal(x,0.1,size=sz) # observations (normal about x, sigma=0.1)
        self.z = np.array(50)

        self.Q = 1e-5 # process variance

        # allocate space for arrays
        self.xhat = np.zeros(self.sz)      # a posteri estimate of x
        self.P = np.zeros(self.sz)         # a posteri error estimate
        self.xhatminus = np.zeros(self.sz) # a priori estimate of x
        self.Pminus = np.zeros(self.sz)    # a priori error estimate
        self.K = np.zeros(self.sz)         # gain or blending factor

        self.R = 0.1**2 # estimate of measurement variance, change to see effect

        # intial guesses
        self.xhat[0] = 0.0
        self.P[0] = 1.0

        self.last = 1e-5

    def kalmanfilter_calculation(self, m_time, m_data):
        self.z = m_data

        if self.last == 1e-5:
            self.x = m_data[0]
        else:
            self.x = self.last

        print("self.x: ", self.x, "length :", self.n_iter, "len(m_data): ", len(m_data))

        self.n_iter = len(m_data)

        for k in range(self.n_iter):
            # time update
            self.xhatminus[k] = self.xhat[k-1]
            self.Pminus[k] = self.P[k-1] + self.Q

            # measurement update
            self.K[k] = self.Pminus[k] / (self.Pminus[k] + self.R)
            self.xhat[k] = self.xhatminus[k] + self.K[k] * (self.z[k] - self.xhatminus[k])
            self.P[k] = (1 - self.K[k]) * self.Pminus[k]

        # self.xhat[0] = self.last
        self.last = self.xhat[-1]

        return self.xhat


# import matplotlib.pyplot as plt
# plt.rcParams['figure.figsize'] = (10, 8)

if __name__ == '__main__':
    print('Connect RMQ')
    rabbitmq = rmq_commumication()
    kalman = kalmanfilter()

    try:
        while(True):
            st = time.time() * 1000

            max_time, max_data = rabbitmq.get()
            if max_time is None:
                time.sleep(0.2)
                continue

            print(max_time, max_data)
            # print("max_time", max_time, "max_data", max_data)

            xhat = kalman.kalmanfilter_calculation(max_time, max_data)
            print(xhat)
            # print(xhat, '\n')
            rabbitmq.publish(max_time, max_data, xhat)

            et = time.time() * 1000
            print("kalman filter elapsed in %2.f" % (et-st))

            # plt.figure()
            # plt.plot(max_data,'k+',label='noisy measurements')
            # plt.plot(xhat,'b-',label='a posteri estimate')
            # # plt.axhline(x,color='g',label='truth value')
            # plt.legend()
            # plt.title('Estimate vs. iteration step', fontweight='bold')
            # plt.xlabel('Iteration')
            # plt.ylabel('Voltage')
            # plt.show()

            
    except(KeyboardInterrupt, Exception) as ex:
        print(ex)
    finally:
        print('Close all')
        rabbitmq.connection.close()


