#! /usr/bin/python3
import sys
from scipy.io import wavfile
import os

import argparse
import pika

import time

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
        self.leftarray = raw[0]  # From two channel wav, get left channel only --> Sync
        self.sync = (self.leftarray > self.thresh)  # An array of True/False --> if leftarray > 0, then true else false
        self.rightarray = raw[1]  # From two channel wav, get right channel only --> received signal
        # print(self.rightarray.shape, self.rightarray.dtype, self.sync.shape)
        data = self.sync.tostring() + self.rightarray.tostring()
        headers = {'sync': len(self.sync.tostring()), 'data': len(self.rightarray.tostring())}
        # print(headers)
        pika_properties = pika.BasicProperties(headers=headers)
        self.connection.publish(
            exchange=EXCHANGE_NAME,
            properties=pika_properties,
            routing_key='raw',
            body=data)


    # def data_assembler(self, raw):
    #     data = bytearray()
    #     self.leftarray = raw[0]  # From two channel wav, get left channel only --> Sync
    #     self.rightarray = raw[1]  # From two channel wav, get right channel only --> received signal
    #     self.sync = (self.leftarray > self.thresh)  # An array of True/False --> if leftarray > 0, then true else false
    #     print(type(self.sync), self.sync.dtype)

    #     rightarray = [ int((x / 2**16) * 2**10) for x in self.rightarray]

    #     for i in range(len(self.sync)):
    #         # if sync is true or false
    #         if self.sync[i] == True:
    #             self.msB = 0x20
    #             # self.msB = 0b00100000
    #         else:
    #             self.msB = 0x00
    #             # self.msB = 0b00000000

    #         # if data is negative of positive
    #         if self.rightarray[i] < 0:
    #             self.msB = self.msB | 0x80
    #             # self.msB = self.msB | 0b10000000

    #         # put a data in the two bytes
    #         self.msB = self.msB | ((abs(self.rightarray[i]) >> 5) & 0x1F)
    #         self.lsB = 0xDF & (abs(self.rightarray[i]) & 0x1F)
    #         # self.lsB = 0b11011111 & (abs(self.rightarray[i]) & 0x1F)

    #         data.append(self.msB)
    #         data.append(self.lsB)

    #     return data


class inwav_handler():
    def __init__(self, file_name):
        self.fs, self.data = wavfile.read(file_name)  # Sampling rate in samples per second (fs), and data
        self.data = self.data.T  # Transposed data
        self.count = 0

    def get_chunk(self):
        # print("Get Chunk")
        if self.count + self.fs < self.data.shape[1]:  # Get a chuck of an array with a length of Sampling rate (fs) from the total data set
            data = self.data[:, self.count : self.count+self.fs]
            self.count += self.fs
            return data
        else:
            return None


if __name__ == "__main__":
    # Read wav file
    # print('Open data file')
    pwd = os.getcwd() # current working folder
    file_name = pwd+ '/' +sys.argv[1]
    inwav = inwav_handler(file_name)

    print('Connect RMQ')
    rabbitmq = rmq_commumication()

    try:
        while(True):
            raw = inwav.get_chunk()
            if raw is None:
                # print('no data to read')
                break
            # data = rabbitmq.data_assembler(raw)
            rabbitmq.publish(raw)
            time.sleep(1)

    except(KeyboardInterrupt, Exception) as ex:
        print(ex)
    finally:
        print('Close all')
        rabbitmq.connection.close()


