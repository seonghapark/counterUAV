#! /usr/lib/python3

from threading import Thread

# import matplotlib.pyplot as plt
# import matplotlib.animation as animation

import matplotlib.colors as colors
from matplotlib.colors import BoundaryNorm

import matplotlib.pylab as plt
from matplotlib import animation

import numpy as np
import sys
import pika
import time
import queue

import argparse

EXCHANGE_NAME = 'radar'

class rmq_commumication(Thread):
    def __init__(self, plotter):
        Thread.__init__(self)
        self.result_time = []
        self.result_data = []
        self.plot = plotter
        self.channel = self.get_connection()
        self.in_queue = self.subscribe(self.channel)


    def get_connection(self, url='amqp://localhost'):
    # def get_connection(self, url='amqp://192.168.20.83'):
    # def get_connection(self, url='amqp://10.31.81.51'):
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


    def run(self):
        print('run')
        self.channel.basic_consume(self._callback, queue=self.in_queue, no_ack=True)
        try:
            self.channel.start_consuming()
        except:
            pass
        # except Exception as ex:
        #     print('oops', str(ex))


    def _callback(self, channel, method, properties, body):
        # print("_callback: ", 'channel: ', channel, ' method: ', method, ' properties: ', properties, ' body: ',body)
        headers = properties.headers
        self.data_disassembler(bytearray(body), headers)
        self.plot.set(self.result_time, self.result_data)


    def data_disassembler(self, body, properties):
        self.result_time = np.fromstring(np.array(body[:properties['result_time']]), dtype=np.float64)

        self.result_data = np.fromstring(np.array(body[properties['result_time']:]), dtype=np.float64)
        self.result_data = np.reshape(self.result_data, (int(len(self.result_time)), int(len(self.result_data)/len(self.result_time))))

        self.plot.set(self.result_time, self.result_data)


class colorgraph_handler():
    def __init__(self):
        ## constants for frame
        # self.n = int(5512/50)  # Samples per a ramp up-time
        # self.n = int(11724/50)/2
        self.n = int(44100/50)
        self.zpad = 8 * (self.n / 2)  # the number of data in 0.08 seconds?
        # self.lfm = [2260E6, 2590E6]  # Radar frequency sweep range
        self.lfm = [2400E6, 2500E6]
        self.max_detect = 3E8/(2*(self.lfm[1]-self.lfm[0]))*self.n/2 # Max detection distance according to the radar frequency
        self.set_t = 10 #int(sys.argv[1])  # Frame length on x axis
        # self.set_t = 25  # Frame length on x axis --> 25 seconds

        ## variables for incoming data
        self.y = np.linspace(0,self.max_detect, int(self.zpad/2))
        self.data_tlen = 0
        self.data_t = np.zeros((50))
        self.data_val = np.zeros((50, self.y.shape[0]))

        self.q_result_data = queue.Queue()
        self.q_result_time = queue.Queue()
        self.previous = 0

        ## constants to plot animation, initialize animate function
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.xlabel = plt.xlabel('Time(s)')
        self.ylabel = plt.ylabel('Distance(m)')
        self.ylim = plt.ylim(0,self.max_detect)
        self.cmap = plt.get_cmap('jet')
        self.norm = colors.BoundaryNorm([i for i in range(-80,1)], ncolors=self.cmap.N, clip=True)
        self.pcolormesh = plt.pcolormesh(self.data_t, self.y, self.data_val.T, cmap=self.cmap, norm=self.norm)
        self.colorbar = plt.colorbar()
        self.colorlabel = self.colorbar.set_label('Intensity (dB)')

        self.processed_time = []

    def set(self, result_time, result_data):
        print('set')
        if self.previous != result_time.item(0):
            self.previous = result_time.item(0)
            self.q_result_time.put(result_time)
            self.q_result_data.put(result_data)

        # print(self.previous, result_time.item(0), type(self.previous), type(result_time.item(0)))
        # time.sleep(0.9)

    def get(self):
        if not self.q_result_time.empty():
            # print('get')
            self.data_t = self.q_result_time.get()
            self.data_val = self.q_result_data.get()

            self.data_tlen = len(self.data_t)

            self.processed_time = []
            for i in range(50):
                temp_time = self.data_t[i] + 0.0016 * (i + 1)
                self.processed_time.append(temp_time)
            self.processed_time = np.array(self.processed_time)

            self.data_t = self.processed_time

            print(self.data_t)

            # print(self.data_t.item(0))
        # print(self.data_t, self.data_val)

    def animate(self, time):
        # print('data', self.data_val, self.data_val.shape)
        self.get()

        time = time+1

        if time >= self.set_t:
            lim = self.ax.set_xlim(time - self.set_t, time)
        else:
            # makes it look ok when the animation loops
            lim = self.ax.set_xlim(0, self.set_t)

        # print(self.data_t.shape, self.data_val.shape, self.data_tlen)
        plt.pcolormesh(self.data_t + (time - 1), self.y, self.data_val[:self.data_tlen].T, cmap=self.cmap, norm=self.norm)
        # print('animate ')

        return self.ax

    def draw_graph(self):
        # ani = animation.FuncAnimation(self.fig, self.animate, init_func=self.animate_init, interval=1000)#, frames=self.set_t, repeat=False)
        # ani = animation.FuncAnimation(self.fig, self.animate, interval=1000, frames=range(0,5))
        ani = animation.FuncAnimation(self.fig, self.animate, interval=1000, blit=False)
        plt.show()


if __name__ == '__main__':
    print('Connect RMQ')
    plot = colorgraph_handler()
    rabbitmq = rmq_commumication(plot)
    # print(rabbitmq.max_detect)

    rabbitmq.start()

    # try:
    while(True):
        st = time.time()*1000
        if plot.q_result_time.empty():
            # print('queue is empty')
            time.sleep(1)
        else:
            # print('queue is not empty')
            break

    et = time.time()*1000
    print("Elapsed in %2.f" % (et-st))

    plot.draw_graph()  # It takes approximately 500 ms

    # except(KeyboardInterrupt, Exception) as ex:
    #     print(ex)
    # finally:
    #     print('Close all')
    #     rabbitmq.channel.close()

