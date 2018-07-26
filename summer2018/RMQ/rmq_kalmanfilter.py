#! /usr/lib/python3
import numpy
import numpy as np
import sys
from scipy.fftpack import fft
import os
import pika
import time

import matplotlib.pyplot as plt
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

    # TODO
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
            #print('max time',max_time)
            # print('max data',max_data)
            #print('max data',len(max_data))
            #print(type(max_data))

            et = time.time()*1000

            # intial parameters
            n_iter = 10 # Number of iterations in Kalman Filter
            kalman = []
                               
            for j in range(len(max_data)):
            #for j in range(50):    
                    #print('x :',max_data[j])
                    #######################################################
                    x = max_data[j] # truth value (typo in example at top of p. 13 calls this z)
                    #######################################################
                    
                    sz = (n_iter,) # size of array        
                    z = numpy.random.normal(x,0.1,size=sz)# 측정 잡음으로 정규분포의 산포 0.1을 가진 랜덤값 z shape :  (50,)
                    Q = 1e-5 # process variance
                    #step1 determine A,H,w,v,Q,R
                    # allocate space for arrays
                    xhat=np.zeros(sz)      # a posteri estimate of x 추정전 ,후 출력 (50,0)
                    P=np.zeros(sz)         # a posteri error estimate
                    xhatminus=np.zeros(sz) # a priori estimate of x
                    Pminus=np.zeros(sz)    # a priori error estimate
                    K=np.zeros(sz)         # gain or blending factor

                    R = 0.1**2 # estimate of measurement variance, change to see effect (상수)

                    # step2 : intial guesses
                    xhat[0] = 0.0 # 예측상태출력값
                    P[0] = 1.0 # 예측공분산 matrix

                    for k in range(1,n_iter):# 반복하여 측정값을 입력받아 추정값 출력               
                        # step3 : time update (predic)
                        xhatminus[k] = xhat[k-1] #project the state ahead x 갱신
                        Pminus[k] = P[k-1]+Q #project the error covariance ahead 다음상태 P = 현재P + 예측노이즈 공분산Q

                        # measurement update (Correct)
                        K[k] = Pminus[k]/( Pminus[k]+R ) #step4 : compute the Kalman gain               
                        xhat[k] = xhatminus[k]+K[k]*(z[k]-xhatminus[k])# Update estimate with measurement z_k
                        #what[k] : 현재예측상태값 , z는 측정잡음
                        P[k] = (1-K[k])*Pminus[k] # Update the eror covariance

                    # print('xhat :',xhat[n_iter-1])#n_iter한 최종값
                    kalman.append(xhat[n_iter - 1])
                    #print('xhatminus :',xhatminus[k])
                    # print('xhatminus :',xhat[n_iter-1])
            # print(max_time)
            rabbitmq.publish(max_time, max_data, kalman)


            
    except(KeyboardInterrupt, Exception) as ex:
        print(ex)
    finally:
        print('Close all')
        rabbitmq.connection.close()