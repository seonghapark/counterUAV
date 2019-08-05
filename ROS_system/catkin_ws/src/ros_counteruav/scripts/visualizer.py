#! /usr/bin/env python3
from flask import Flask,Response
import rospy
from ros_counteruav.msg import result
from threading import Thread
import io
import random

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
#from std_msgs.msg import String
import matplotlib.pyplot as plt
# import matplotlib.animation as animation

import matplotlib.colors as colors
from matplotlib.colors import BoundaryNorm

#import matplotlib.pyplot as plt
from matplotlib import animation

import numpy as np
import sys
import pika
import time
import queue

import argparse

app = Flask(__name__)
result_time = []
result_data = []
q_result_data = queue.Queue()
q_result_time = queue.Queue()

class ros_service(Thread):
    def __init__(self,plotter) :
        global result_time
        global result_data
        self.result_time = []
        self.result_data = []
        self.plot = plotter
        

    def callback(self,data):
        print('START callback')
        self.data_disassembler(data)
        # global result_time
        # global result_data
        # self.plot.set(self.result_time, self.result_data)
        print('FINISH callback')
        #return Response(status=400)

    def listener(self):
        #print('listener START')
        rospy.init_node('visualizer_receiver', anonymous=True)
        rospy.Subscriber('analyzed_data', result, self.callback)
        print('BEFORE spin')
        rospy.spin()
        print('AFTER spin')
    
    # def _callback(self, channel, method, properties, body):
    #     print("_callback: ", 'channel: ', channel, ' method: ', method, ' properties: ', properties, ' body: ',body)
    #     self.data_disassembler(bytearray(body))
    #     self.plot.set(self.result_time, self.result_data)


    def data_disassembler(self, body):
        #self.result_time = np.fromstring(np.array(body[:properties['result_time']]), dtype=np.float64)
        print('disassembler START')
        global result_time
        global result_data

        self.result_time = np.fromstring(body.time, dtype=np.float64)
        print(self.result_time)       
        self.result_data = np.fromstring(body.data, dtype=np.float64)
        self.result_data = np.reshape(self.result_data, (int(len(self.result_time)), int(len(self.result_data)/len(self.result_time))))
        self.plot.set(self.result_time, self.result_data) 

class colorgraph_handler(Thread):
    def __init__(self):
        Thread.__init__(self)
        ## constants for frame
        self.n = int(5512/50)  # Samples per a ramp up-time
        # self.n = int(5512/50)
        # self.zpad = 8 * (self.n / 2)  # the number of data in 0.08 seconds?
        #self.zpad = 468 * 2
        self.zpad = 468 * 2
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

    def get_fig(self):
        return self.fig

    global result_time
    global result_data
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

            # print(self.data_t.item(0))
        # print(self.data_t, self.datFa_val)

    def animate(self, time):
        # print('data', self.data_val, self.data_val.shape)
        print('animate START')
        print('get BEFORE')
        self.get()
        print('get AFTER')

        time = time+1

        if time > self.set_t:
            lim = self.ax.set_xlim(time - self.set_t, time)
        else:
            # makes it look ok when the animation loops
            lim = self.ax.set_xlim(0, self.set_t)

        # print(self.data_t.shape, self.data_val.shape, self.data_tlen)
        plt.pcolormesh(self.data_t, self.y, np.swapaxes(self.data_val[:self.data_tlen], 0, 1), cmap=self.cmap, norm=self.norm)
        plt.draw()
        #plt.show()
        return self.ax

    def draw_graph(self):
        print('draw_graph START')
        print(self.q_result_time)
        # ani = animation.FuncAnimation(self.fig, self.animate, init_func=self.animate_init, interval=1000)#, frames=self.set_t, repeat=False)
        # ani = animation.FuncAnimation(self.fig, self.animate, interval=1000, frames=range(0,5))
        ani = animation.FuncAnimation(self.fig, self.animate, interval=1000, blit=False)
        plt.show()
        print('draw_graph FINISH')

    def run(self) :
        try:
            while(True):
                print('while START')
                # print('main while(True)')
                if self.q_result_time.empty():
                    print('queue is empty')
                    time.sleep(1)
                else:
                    # print('queue is not empty')
                    print('while FINISH')
                    break

            # print('while(False)')

            self.draw_graph()  # It takes approximately 500 ms

        except(KeyboardInterrupt, Exception) as ex:
            print(ex)
        finally:
            print('Close all')
            #rabbitmq.channel.close()
            
class web_service(Thread):
    def __init__(self) :
        Thread.__init__(self)

    def run(self):
        print('run')
        global app
        app.run(host='localhost',port='8080')
@app.route('/')
def show_graph():
    return render_template('show_graph.html')

@app.route('/plot')
def plot_png():
    # while(True):
    #     if not plot.q_result_time.empty():
    fig = plot.get_fig()
    output = io.BytesIO()
    FigureCanvas(fig).print_figure(output)
    #return render_template('show_graph.html', )
    return Response(output.getvalue(), mimetype='image/png')
        # else:
        #     time.sleep(1)
    #fig = create_figure()
    #FigureCanvas(fig).print_png(output)    
    # output = io.BytesIO()
    # canvas = FigureCanvas(plot.get_fig())
    # canvas.print_figure('app', dpi=150)
    # return Response(canvas.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

@app.route("/hello/")
def hello():                           
    return "<h1>Hello World!</h1>"


if __name__=='__main__':
    plot = colorgraph_handler()
    web = web_service()
    ros = ros_service(plot)
    web.start() 
    plot.start()
    ros.listener()