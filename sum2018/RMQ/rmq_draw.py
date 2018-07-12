#! /usr/lib/python3

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation
from matplotlib.colors import BoundaryNorm

import numpy as np
import sys
import pika
import time
import queue

EXCHANGE_NAME = 'radar'

class rmq_commumication():
    def __init__(self):
        self.data_time = []
        self.result = []
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
            routing_key='ifft'
        )
        return in_queue


    def publish(self, data_time, result):
        data = data_time.tostring() + result.tostring()
        headers = {'date_time': len(data_time.tostring()), 'result': len(result.tostring())}
        pika_properties = pika.BasicProperties(headers=headers)
        self.connection.publish(
            exchange=EXCHANGE_NAME,
            properties=pika_properties,
            routing_key='ifft',
            body=data)


    def get(self):
        method, properties, body = self.connection.basic_get(queue=self.in_queue, no_ack=True)

        if method is None:
            return None, None

        headers = properties.headers
        self.data_disassembler(bytearray(body), headers)

        return self.result_time, self.result_data


    def data_disassembler(self, body, properties):
        self.result_time = np.fromstring(np.array(body[:properties['result_time']]), dtype=float)

        self.result_data = np.fromstring(np.array(body[properties['result_time']:]), dtype=float)
        self.result_data = np.reshape(self.result, (int(len(self.result_time)), int(len(self.result)/len(self.result_time))))


class colorgraph_handler():
    def __init__(self):
        self.n = 882  # Samples per a ramp up-time
        self.zpad = 3528  # the number of data in 0.08 seconds?
        self.lfm = [2260E6, 2590E6]  # Radar frequency sweep range
        self.max_detect = 3E8/(2*(self.lfm[1]-self.lfm[0]))*self.n/2 # Max detection distance according to the radar frequency
        self.set_t = int(sys.argv[1])  # Frame length on x axis
        # self.set_t = 25  # Frame length on x axis --> 25 seconds

        self.y = np.linspace(0,self.max_detect, int(self.zpad/2))
        self.data_tlen = 0
        self.data_t = np.zeros((300))
        self.data_val = np.zeros((300, self.y.shape[0]))

        self.q_result_data = queue.Queue()
        self.q_result_time = queue.Queue()

        # self.in_t = open("time_ndarray.txt","r")
        # self.in_val = open("val_ndarray.txt","r")

        self.fig = plt.figure()

    def set(self, result_time, result_data):
        self.q_result_time.put(result_time)
        self.q_result_data.put(result_data)
        # self.data_t = data_time
        # self.data_val = result
        # self.data_tlen = len(self.data_t)
        # print(result)
        # print(self.data_val)
        # self.data_val[val_l] = np.array(split_line)

    def get(self):
        if not q_result_time.empty():
            self.data_t = q_result_time.get()
            self.data_val = q_result_data.get()
        self.data_tlen = len(self.data_t)

    def animate_init(self):
        plt.xlabel('Time(s)')
        plt.ylabel('Distance(m)')
        plt.ylim(0,self.max_detect)

        self.cmap = plt.get_cmap('jet')
        self.norm = BoundaryNorm([i for i in range(-80,1)], ncolors=self.cmap.N, clip=True)
        plt.pcolormesh(self.data_t, self.y, self.data_val.T, cmap=self.cmap, norm=self.norm)
        plt.colorbar()

    def animate(self, time):
        # print('data', self.data_val, self.data_val.shape)
        self.get()
        plt.pcolormesh(self.data_t, self.y, self.data_val[:self.data_tlen].T, cmap=self.cmap, norm=self.norm)
        plt.xlim(time - self.set_t + 1, time + 1)

    def draw_graph(self):
        ani = animation.FuncAnimation(self.fig, self.animate, init_func=self.animate_init, interval=1000, frames=self.set_t, repeat=False)
        plt.show()



if __name__ == '__main__':  
    print('Connect RMQ') 
    rabbitmq = rmq_commumication()
    plot = colorgraph_handler()

    init_draw = False

    try:
        count = 0
        while(True):
            result_time, result_data = rabbitmq.get()

            if result_time is None:
                # print('no incomming data', result)
                time.sleep(0.5)
                continue

            st = time.time()*1000
            plot.set(result_time, result_data)
            
            if init_draw == False:
                plot.draw_graph()  # It takes approximately 500 ms

            et = time.time()*1000
            print('Drawing elapsed in %2.f' % (et-st))
            count+=1

        #         rabbitmq.publish(data_time, result)

    except(KeyboardInterrupt, Exception) as ex:
        print(ex)
        plt.close('all')
    finally:
        print('Close all')
        plt.cloat('all')
        rabbitmq.connection.close()


