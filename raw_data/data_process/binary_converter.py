#! /usr/lib/python3

import numpy as np
import sys
from scipy.fftpack import fft
from scipy.io import wavfile
import librosa
import os
import pika

import time

EXCHANGE_NAME = 'radar'


class rmq_commumication():
    def __init__(self):
        # self.sync = np.array([])
        # self.data = np.array([])
        # self.sign = 0
        self.connection = self.get_connection()
        self.in_queue = self.subscribe (self.connection)

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
            routing_key='raw'
        )
        return in_queue


    def publish(self, result_time, result_data):
        data = result_time.tostring() + result_data.tostring()
        # pika_properties = pika.BasicProperties(content_type='application/json', headers=headers)
        self.connection.publish(
            exchange=EXCHANGE_NAME,
            # properties=pika_properties,
            routing_key='ifft',
            body=data)

    '''
        get sync, data and headers from rmq message.
        headers include index of chunk(index), total length(length), file name(name)
    '''
    def get(self):
        method, properties, body = self.connection.basic_get(queue=self.in_queue, no_ack=True)

        if method is None:
            return None, None, None

        headers = properties.headers
        data = bytearray(body)
        # print(len(data))

        # parse the sync and data signal in bytearray
        if len(data) < 2:
            return None, None
        if (data[0] >> 6) > 0:
            del data[:1]
        if len(data) % 2 == 1:
            del data[-1:]

        values = []
        sync = []
        for index in range(0, len(data), 2):
            high = data[index] & 0x1F
            low = data[index + 1] & 0x1F
            values.append(high << 5 | low)  
            sync.append(True if (data[index] >> 5) == 1 else False)

        self.sync = np.array(sync)
        self.data = np.array(values)
        
        # print(self.sync, self.data, len(self.sync), len(self.data))
        return self.sync, self.data, headers

if __name__ == '__main__':  
    print('Connect RMQ') 
    rabbitmq = rmq_commumication()
    audio = np.array([]).reshape((2, -1))

    print('Start to read... ') 
    while(True):
        sync, data, headers = rabbitmq.get()
        if sync is None:
            # print('no incoming data', data)
            time.sleep(0.1)
            continue
        else:
            # stacking audio data 
            print('sync: ', sync, ' data: ', data)
            print('get: ', len(sync), len(data))
            np_sync = np.array(sync, dtype=np.bool)
            np_data = np.array(data, dtype=np.int16)
            temp = np.vstack((sync, data))
            audio = np.hstack((audio, temp))
            # print(audio.shape[1])

        # write a wav file when it finish reading binary data
        if audio.shape[1] > 5862 * (headers['length'] - 1) :
            print('audio: ', audio.shape)
            wavfile.write(headers['name'] + ".wav", 5862, audio.T.astype(np.int16))
            #audio = np.array([]).reshape((2, -1))
            print('Finish to read... ')
            break
            
    rabbitmq.connection.close()
    print('Close RMQ')
