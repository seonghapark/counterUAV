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
        # self.sync = np.array([])
        # self.data = np.array([])
        # self.sign = 0
        self.connection = self.get_connection()
        self.in_queue = self.subscribe(self.connection)

    def get_connection(self, url='amqp://localhost'):
    # def get_connection(self, url='amqp://192.168.20.83'):
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
        headers = {'result_time': len(result_time.tostring()), 'result': len(result_data.tostring())}
        pika_properties = pika.BasicProperties(headers=headers)
        # pika_properties = pika.BasicProperties(content_type='application/json', headers=headers)
        self.connection.publish(
            exchange=EXCHANGE_NAME,
            properties=pika_properties,
            routing_key='ifft',
            body=data)


    def get(self):
        method, properties, body = self.connection.basic_get(queue=self.in_queue, no_ack=True)

        if method is None:
            return None, None

        data = bytearray(body)
        print(len(data))

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

        # print(self.sync.shape, self.sync, self.data)
        return self.sync, self.data


class ifft_handler():
    def __init__(self):
        self.opp = 0
        # self.fs = 44100  # Sampling rate
        self.fs = 11724
        self.Tp = 0.020   # Radar ramp up-time
        self.n = int(self.Tp*self.fs)   # Samples per ramp up-time
        self.fsif = np.zeros([10000,self.n], dtype=np.int16)  # Zero array for further data storage

    def dbv(self, input):
        input = input + 0.0000001
        return 20 * np.log10(abs(input))  # Calculate Decibel using received signal intensity value


    def data_process(self, sync, data):
        count = 0
        result_time = [] # time is a list
        self.fs = len(sync)
        self.n = int(self.Tp*self.fs)
        self.fsif = np.zeros([10000,self.n], dtype=np.int16) 
        # print(self.fs)

        # print(data, data.shape, self.n)
        # print(sync, sync.shape)

        spliter = 50 # to search rising edge
        val = 2
        for ii in range(val, int((sync.shape[0] - self.n)), spliter):  # improved searching loop
            # if sync[ii - 11 - spliter:ii - spliter] == []:
            #     continue
            if (ii - spliter > 0) & (sync[ii] == True) & (sync[ii - val - spliter:ii - spliter].max() == False):  # if start[ii] is true and the mean of from start[ii-11] to start[ii-1] is zero (All False)
                for jj in range(ii - spliter, ii):
                    if (sync[jj] == True) & (sync[jj - val:jj - 1].mean() == 0.0):
                        # print(data[jj:jj + self.n], jj)
                        # print(self.n)
                        self.fsif[count, :] = data[jj:jj + self.n]  # then copy rightarray from ii to ii+n and paste them to sif[count] --> sif[count] is a list
                        result_time.append((jj + int(sync.shape[0]) * self.opp) * 1. / self.fs)  # append time, the time is ii/fs --> few micro seconds (0.0001 sec or so)
                        count = count + 1

                        self.fsif[count, :] = data[jj + 1:jj + 1 + self.n]  # then copy rightarray from ii to ii+n and paste them to sif[count] --> sif[count] is a list
                        result_time.append((jj + 1 + int(sync.shape[0]) * self.opp) * 1. / self.fs)  # append time, the time is ii/fs --> few micro seconds (0.0001 sec or so)
                        count = count + 1

                        break

        # self.opp += 1
        result_time = []
        for i in range(50):
            result_time.append(self.Tp * (i + 1))

        result_time = np.array(result_time)  # change the format of time from list to to np.array
        sif = self.fsif[:count,:] # truncate sif --> remove all redundant array lists in sif, just in case if sif is longer then count
        sif = sif - np.tile(sif.mean(0), [sif.shape[0], 1])
        zpad = int(8 * self.n / 2)  # create the number_of_ifft_entities --> which is the number of vales that has to be created from fft calculation
        decibel = self.dbv(np.fft.ifft(sif, zpad, 1)) # Do fft calculation, and convert results to decibel through dbv function
        real_value = decibel[:,0:int(decibel.shape[1] / 2)] 
        max_real = real_value.max() 
        result_data = real_value - max_real

        #### 2 pulse cancelor RTI plot
        sif2 = sif[1:sif.shape[0],:] - sif[:sif.shape[0]-1,:]
        last = sif[-1,:]
        sif2 = np.vstack((sif2, last))
        # print(sif2, sif2.shape, sif.shape, zpad)
        v = np.fft.ifft(sif2, zpad, 1)
        decibel = self.dbv(v)
        real_value = decibel[:,0:int(decibel.shape[1] / 2)]
        max_real = real_value.max() 
        result_data = real_value - max_real

        print(len(result_time), len(result_data))

        result_time = result_time[:50]
        result_data = result_data[:50]

        print(result_time, result_data)
        print(result_time.shape, result_data.shape)
        # print(result_time.dtype, result_data.dtype)
        return result_time, result_data


if __name__ == '__main__':  
    print('Connect RMQ') 
    rabbitmq = rmq_commumication()
    ifft = ifft_handler()

    # out_t = open('fft_result_time.txt','w+')   # Create a file
    # out_sm = open('fft_result_data.txt','w+')   # Create a file

    # try:
    while(True):
        sync, data = rabbitmq.get()
        if sync is None:
            # print('no incomming data', data)
            time.sleep(0.2)
            continue
        # else:
        #     print('sync: ', sync, ' data: ', data)

        st = time.time()*1000
        result_time, result_data = ifft.data_process(sync, data)  # It takes approximately 500 ms
        et = time.time()*1000
        # print('FFT elapsed in %2.f' % (et-st), result_time.shape, result_data.shape)

        rabbitmq.publish(result_time, result_data)
        # print(result_data)

        # for k in range(0,len(result_time)):
        #     out_t.write(str(result_time[k])+', ')
        #     out_t.write("\n")
        #     out_t.flush()
        # for k in range(0,len(result_data)):
        #     out_sm.write(str(result_data[k])+', ')
        #     out_sm.write("\n")
        #     out_sm.flush()

    # except(KeyboardInterrupt, Exception) as ex:
    #     print(ex)
    # finally:
    #     print('Close all')
    #     rabbitmq.connection.close()


