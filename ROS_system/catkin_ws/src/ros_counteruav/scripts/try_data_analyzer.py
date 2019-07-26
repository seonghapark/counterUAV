#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import sys
from scipy.fftpack import fft

import os
import pika

import time
import rospy
#from std_msgs.msg import String
from ros_counteruav.msg import fakedata

body = ''

class data_analyzer():
    def __init__(self):
        self.sync = 0
        self.real_data=0

            
    def get_sync(self):
        return self.sync
    
    def get_real_data(self):
        return self.real_data
    
    def listener(self):
        print('listener func START')
        rospy.init_node('analyzer_reciever', anonymous=True)
        rospy.Subscriber('msg_for_analyzer', fakedata, self.callback)
        rospy.spin()
        print('AFTER spin')

    
    def callback(self, data):
        ###########################get()#############################
        real_data = bytearray(data.data)
        print('Data length:', len(real_data))

        if len(real_data) < 2:
            self.sync = None
            self.real_data = None

        if (real_data[0] >> 6) > 0:
            del real_data[:1]
            values = []
            sync = []
            for index in range(0, len(real_data), 2):
                high = int(real_data[index]) & 0x1F
                low = int(real_data[index + 1]) & 0x1F
                values.append(high << 5 | low)
                sync.append(True if (real_data[index] >> 5) == 1 else False)

            self.sync = np.array(sync)
            self.real_data = np.array(values)
            
        if len(real_data) % 2 == 1:
            del real_data[-1:]
            values = []
            sync = []
            for index in range(0, len(real_data), 2):
                high = int(real_data[index]) & 0x1F
                low = int(real_data[index + 1]) & 0x1F
                values.append(high << 5 | low)
                sync.append(True if (real_data[index] >> 5) == 1 else False)
            self.sync = np.array(sync)
            self.real_data = np.array(values)


        ############################ ifft ###############################
        sync = analyzer.get_sync()
        data = analyzer.get_real_data()
        if sync is None:
            time.sleep(0.2)

        st = time.time()*1000
        print('BEFORE ifft')
        result_time, result_data = ifft.data_process(sync, data)  # It takes approximately 500 ms
        et = time.time()*1000
        print('AFTER ifft')
        analyzer.publish(result_time, result_data)

    def publish(self, result_time, result_data):
        print('publish START')
        Analyzed_data = result_time.tostring() + result_data.tostring()
        analyze_pub = rospy.Publisher('analyzed_data', fakedata, queue_size=10)
        Re_rate = rospy.Rate(10)
        MSG = fakedata()
        MSG.data = Analyzed_data
            
        try:
            rospy.loginfo(str(MSG.data))
            analyze_pub.publish(MSG)
            Re_rate.sleep()
        except(KeyboardInterrupt, Exception) as ex:
            print(ex)
        finally:
            print('publisher Finish')

class ifft_handler():
    def __init__(self):
        self.opp = 0
                #self.fs = 44100  # Sampling rate
        self.fs = 11724
        self.Tp = 0.020   # Radar ramp up-time
        self.n = int(self.Tp*self.fs)   # Samples per ramp up-time
        self.fsif = np.zeros([10000,self.n], dtype=np.int16)  # Zero array for further data storage

    def dbv(self, inp):

        """
            # print("Input to method dbv:", inp)
            # print("Zero values in input:", inp == 0)
            if np.any(inp == 0):
            # Remove any zero values from the input to eradicate divide by zero warning
                min_nonzero = np.min(inp[np.nonzero(inp)])
                inp[inp == 0] = min_nonzero
        """
        return 20 * np.log10(abs(inp))  # Calculate Decibel using received signal intensity value


    def data_process(self, sync, data):
        count = 0
        result_time = [] # time is a list
                # self.fs = len(sync)
        self.n = int(self.Tp*self.fs)
        self.fsif = np.zeros([10000,self.n], dtype=np.int16)
                # print(self.fs)

                # print(data, data.shape, self.n)
                # print(sync, sync.shape)

        spliter = 10 # to search rising edge
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

        self.opp += 1
        result_time = np.array(result_time)  # change the format of time from list to to np.array
        sif = self.fsif[:count,:] # truncate sif --> remove all redundant array lists in sif, just in case if sif is longer then count
        sif = sif - np.tile(sif.mean(0), [sif.shape[0], 1])
        zpad = int(8 * self.n / 2)  # create the number_of_ifft_entities --> which is the number of vales that has to be created from fft calculation
        decibel = self.dbv(np.fft.ifft(sif, zpad, 1)) # Do fft calculation, and convert results to decibel through dbv function
        #print('first decibel : ' + str(decibel))
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
        #print('second decibel : ' + str(decibel))
        real_value = decibel[:,0:int(decibel.shape[1] / 2)]
        max_real = real_value.max()
        result_data = real_value - max_real

        result_time = result_time[:50]
        result_data = result_data[:50]

                # print(result_time.dtype, result_data.dtype)
        return result_time, result_data


if __name__ == '__main__':
    print('Analyzer start')
    global analyzer
    analyzer = data_analyzer()
    global ifft 
    ifft = ifft_handler()
    print('init done')

    analyzer.listener()
    print('listener fucn FINISH')


