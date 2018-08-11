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
        self.max_time = []
        self.max_data = []
        self.particle_data = []
        self.plot = plotter

        self.channel = self.get_connection()
        self.in_queue = self.subscribe(self.channel)


    def get_connection(self, url='amqp://localhost'):
    # def get_connection(self, url='amqp:192.168.2.177'):
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
            routing_key='particle'
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
        if method is None:
            return None

        headers = properties.headers

        if len(body) != 0:
            self.max_time = np.fromstring(np.array(body[:headers['max_data']]), dtype=np.float64)
            self.max_data = np.fromstring(np.array(body[headers['max_data']:]), dtype=np.float64)
            self.particle_data = self.max_data[len(self.max_time):]
            self.max_data = self.max_data[:len(self.max_time)]

        self.plot.set(self.max_time, self.max_data, self.particle_data)



class scattergraph_handler():
    def __init__(self):
        ## constants for frame
        self.n = 882  # Samples per a ramp up-time
        # self.n = int(5512/50)
        self.zpad = 8 * (self.n / 2)  # the number of data in 0.08 seconds?
        # self.lfm = [2260E6, 2590E6]  # Radar frequency sweep range
        self.lfm = [2400E6, 2500E6]
        self.max_detect = 3E8/(2*(self.lfm[1]-self.lfm[0]))*self.n/2 # Max detection distance according to the radar frequency
        self.set_t = 10 #int(sys.argv[1])  # Frame length on x axis
        # self.set_t = 25  # Frame length on x axis --> 25 seconds

        ## variables for incoming data
        self.y = np.linspace(0,self.max_detect, int(self.zpad/2))
        self.data_tlen = 0
        self.data_t = []    # modified
        self.data_val = []
        # self.data_val = np.zeros((50, self.y.shape[0]))
        self.data_particle = []

        self.q_result_data = queue.Queue()
        self.q_result_time = queue.Queue()

        self.q_max_data = queue.Queue()
        self.q_max_time = queue.Queue()
        self.q_particle_data = queue.Queue()

        self.previous = 0

        ## constants to plot animation, initialize animate function
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.xlabel = plt.xlabel('Time(s)')
        self.ylabel = plt.ylabel('Distance(m)')
        self.ylim = plt.ylim(0,self.max_detect)
        # self.ylim = plt.ylim(0,100)
        self.cmap = plt.get_cmap('jet')
        self.norm = colors.BoundaryNorm([i for i in range(-80,1)], ncolors=self.cmap.N, clip=True)


    def set(self, max_time, max_data, particle_data):
        print('set')
        self.q_max_data.put(max_data)
        self.q_max_time.put(max_time)
        self.q_particle_data.put(particle_data)

    def get(self):
        if not self.q_max_time.empty():
            self.data_t = self.q_max_time.get()
            self.data_val = self.q_max_data.get()
            self.data_particle = self.q_particle_data.get()

    def animate(self, time):
        self.get()
        time = time+1

        if time > self.set_t:
            lim = self.ax.set_xlim(time - self.set_t, time)
        else:
            # makes it look ok when the animation loops
            lim = self.ax.set_xlim(0, self.set_t)

        # print(len(self.data_t), len(self.data_val))
        # plt.pcolormesh(self.data_t, self.y, self.data_val[:self.data_tlen].T, cmap=self.cmap, norm=self.norm)


        # draw points of threshold data in color red and draw points of particle filter in green
        plt.scatter(self.data_t, self.data_val, marker='o', s=1, c='red', edgecolor='red')
        plt.scatter(self.data_t, self.data_particle, marker='o', s=1, c='green', edgecolor='green')

        # plt.plot(self.data_t, self.data_particle, c='blue')
        # plt.scatter(self.data_t, self.data_val, marker='o', s=1, c='red', edgecolor='red')

        return self.ax

    def draw_graph(self):
        # ani = animation.FuncAnimation(self.fig, self.animate, init_func=self.animate_init, interval=1000)#, frames=self.set_t, repeat=False)
        # ani = animation.FuncAnimation(self.fig, self.animate, interval=1000, frames=range(0,5))
        ani = animation.FuncAnimation(self.fig, self.animate, interval=1000, blit=False)
        plt.show()


if __name__ == '__main__':
    print('Connect RMQ')
    splot = scattergraph_handler()
    rabbitmq = rmq_commumication(splot)
    rabbitmq.start()

    try:
        while(True):
            # print('main while(True)')
            if splot.q_max_data.empty():
                # print('queue is empty')
                time.sleep(1)
            else:
                # print('queue is not empty')
                break

        # print('while(False)')

        splot.draw_graph()  # It takes approximately 500 ms

    except(KeyboardInterrupt, Exception) as ex:
        print(ex)
    finally:
        print('Close all')
        rabbitmq.channel.close()

