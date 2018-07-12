import matplotlib.pyplot as plt
import numpy as np
import sys
# import zmq
from scipy.io import wavfile
from scipy.fftpack import fft

import os
from threading import Thread
import queue

import time as t

fs = 44100
q_raw= queue.Queue()  # FIFO queue First In First Out
q_result_data = queue.Queue()
q_result_time = queue.Queue()

class inwav_handler(Thread):
    def __init__(self, file_name):
        Thread.__init__(self)
        self.fs, self.data = wavfile.read(file_name)  # Sampling rate in samples per second (fs), and data
        self.data = self.data.T  # Transposed data
        self.count = 0

    def run(self):
        while(True):
            t.sleep(1)
            chunk = self.get_chunk()
            q_raw.put(chunk)
            if chunk is None:
                break

    def get_chunk(self):
        # print("Get Chunk")
        if self.count + fs < self.data.shape[1]:  # Get a chuck of an array with a length of Sampling rate (fs) from the total data set
            data = self.data[:, self.count : self.count+fs]
            self.count += fs
            return data
        else:
            return None

class fft_handler(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.opp = 0
        self.fs = fs  # Sampling rate
        self.Tp = 0.020   # Radar ramp up-time
        self.n = int(self.Tp*self.fs)   # Samples per ramp up-time
        self.fsif = np.zeros([10000,self.n], dtype=np.int16)  # Zero array for further data storage

        # self.out_t = open("time_ndarray.txt","w")   # Create a file
        # self.out_sm = open("val_ndarray.txt","w")   # Create a file

    def run(self):
        count = 0
        while(True):
            raw = q_raw.get()
            if raw is None:
                break
            self.get_line(raw)
            time, result = self.data_process()  # It takes approximately 500 ms
            self.store_result()
            print("in fft", count, time.shape, result.shape)
            count+=1

    def dbv(self, input):
        return 20 * np.log10(abs(input))  # Calculate Decibel using received signal intensity value

    def get_line(self, raw):
        self.leftarray = raw[0]  # From two channel wav, get left channel only --> Sync
        self.rightarray = raw[1]  # From two channel wav, get right channel only --> received signal
        print("left: ", self.leftarray[100:200])
        print("right: ", max(self.rightarray))
        thresh = 0  # Threshold for Sync is 0 Voltage
        self.start = (self.leftarray > thresh)  # An array of True/False --> if leftarray > 0, then true else false

    def data_process(self):
        st = t.time()*1000

        count = 0
        time = [] # time is a list
        for ii in range(11, int((self.start.shape[0]-self.n))): 
            if (self.start[ii] == True) & (self.start[ii-11:ii-1].mean() == 0): # if start[ii] is true and the mean of from start[ii-11] to start[ii-1] is zero
                self.fsif[count,:] = self.rightarray[ii:ii+self.n] # then copy rightarray from ii to ii+n and paste them to sif[count] --> sif[count] is a list
                time.append((ii + int(self.start.shape[0])*self.opp) * 1. / self.fs) # append time, the time is ii/fs --> few micro seconds (0.0001 sec or so)
                count = count + 1
        self.opp+=1

        self.time=np.array(time)  # change the format of time from list to to np.array
        sif = self.fsif[:count,:] # truncate sif --> remove all redundant array lists in sif, just in case if sif is longer then count
        sif = sif-np.tile(sif.mean(0), [sif.shape[0],1])
        zpad = int(8*self.n/2)  # create the number_of_ifft_entities --> which is the number of vales that has to be created from fft calculation
        v = self.dbv(np.fft.ifft(sif, zpad,1)) # Do fft calculation, and convert results to decibel through dbv function
        s = v[:,0:int(v.shape[1]/2)] 
        m = s.max() 
        self.s= s-m

        et = t.time()*1000
        print("fft elapsed in %2.f" %(et-st))

        self.time = self.time[:50]
        self.s = self.s[:50]
        return self.time, self.s

    def store_result(self):
        q_result_time.put(self.time)
        q_result_data.put(self.s)

        # for k in range(0,len(self.time)):
        #     self.out_t.write(str(self.time[k])+' ')
        # self.out_t.write("\n")
        # self.out_t.flush()

        # for kk in range(0,self.s.shape[0]):
        #     for pp in range(0,self.s.shape[1]):
        #         self.out_sm.write(str(self.s[kk][pp])+' ')
        #     self.out_sm.write("\n")
        #     self.out_sm.flush()


import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation
from matplotlib.colors import BoundaryNorm

class colorgraph_handler:
    def __init__(self):
        self.n = 882  # Samples per a ramp up-time
        self.zpad = 3528  # the number of data in 0.08 seconds?
        self.lfm = [2260E6, 2590E6]  # Radar frequency sweep range
        self.max_detect = 3E8/(2*(self.lfm[1]-self.lfm[0]))*self.n/2 # Max detection distance according to the radar frequency
        print("max detection", self.max_detect)
        self.set_t = int(sys.argv[2])  # Frame length on x axis
        # self.set_t = 25  # Frame length on x axis --> 25 seconds

        self.y = np.linspace(0,self.max_detect, int(self.zpad/2))
        self.data_tlen = 0
        self.data_t = np.zeros((300))
        self.data_val = np.zeros((300, self.y.shape[0]))

        # self.in_t = open("time_ndarray.txt","r")
        # self.in_val = open("val_ndarray.txt","r")

        self.fig = plt.figure()

    def get_line(self, time):
        if not q_result_time.empty():
            self.data_t = q_result_time.get()
            self.data_val = q_result_data.get()

        self.data_tlen = len(self.data_t)

    def animate_init(self):
        plt.xlabel('Time(s)')
        plt.ylabel('Distance(m)')
        plt.ylim(0,self.max_detect)

        self.cmap = plt.get_cmap('jet')
        self.norm = BoundaryNorm([i for i in range(-80,1)], ncolors = self.cmap.N, clip = True)
        plt.pcolormesh(self.data_t, self.y, self.data_val.T, cmap = self.cmap, norm = self.norm)
        plt.colorbar()

    def animate(self, time):
        print("Renew graph")
        self.get_line(time)
        plt.pcolormesh(self.data_t, self.y, self.data_val[:self.data_tlen].T, cmap = self.cmap, norm = self.norm)
        plt.xlim(time-self.set_t+1, time+1)

    def draw_graph(self):
        t.sleep(5)
        ani = animation.FuncAnimation(self.fig, self.animate, init_func = self.animate_init, interval=1000, frames = self.set_t, repeat = False)
        plt.show()



