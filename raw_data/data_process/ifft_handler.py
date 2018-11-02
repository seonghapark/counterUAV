#! /usr/lib/python3

import numpy as np
import sys
from scipy.fftpack import fft

import os
import time


class ifft_handler():
    def __init__(self, sr=5862, ramp_time=0.020):
        # self.fs = 44100
        # Sampling rate
        self.fs = s
        # Radar ramp up-time
        self.Tp = ramp_time
        # Samples per ramp up-time
        self.n = int(self.Tp * self.fs)
        # Zero array for further data storage
        self.fsif = np.zeros([10000, self.n], dtype=np.int16)

    '''
    Calculate Decibel using received signal intensity value
    '''
    def dbv(self, input):
        return 20 * np.log10(abs(input))

    '''
    Return range time intensity data(time, data).
    '''
    def data_process(self, sync, data):
        result_time = []  # time is a list
        # print('n: ', self.n)
        self.fsif = np.zeros([10000, self.n], dtype=np.int16)
        # print(self.fs)
        # print(data, data.shape, self.n)
        # print(sync, sync.shape)

        spliter = 10  # to search rising edge
        val = 2
        count = 0
        # improved searching loop
        for ii in range(val, int((sync.shape[0] - self.n)), spliter):
            # if sync[ii - 11 - spliter:ii - spliter] == []:
            #     continue

            # if start[ii] is true and the mean of from start[ii-11] to start[ii-1] is zero (All False)
            if (ii - spliter > 0) & (sync[ii] == True) & (sync[ii - val - spliter:ii - spliter].max() == False):  
                for jj in range(ii - spliter, ii):
                    if (sync[jj] == True) & (sync[jj - val:jj - 1].mean() == 0.0):
                        # print(data[jj:jj + self.n], jj)
                        # print(self.n)

                        # then copy rightarray from ii to ii+n and paste them to sif[count] --> sif[count] is a list
                        self.fsif[count, :] = data[jj:jj + self.n]

                        # append time, the time is ii/fs --> few micro seconds (0.0001 sec or so)
                        result_time.append(float(jj) / self.fs)  
                        count = count + 1

                        # then copy rightarray from ii to ii+n and paste them to sif[count] --> sif[count] is a list
                        self.fsif[count, :] = data[jj + 1:jj + 1 + self.n]

                        # append time, the time is ii/fs --> few micro seconds (0.0001 sec or so)
                        result_time.append(float(jj + 1) / self.fs)
                        count = count + 1

                        break

        # change the format of time from list to to np.array
        result_time = np.array(result_time)

        # truncate sif --> remove all redundant array lists in sif, just in case if sif is longer then count
        sif = self.fsif[:count, :] 
        sif = sif - np.tile(sif.mean(0), [sif.shape[0], 1])

        # create the number_of_ifft_entities --> which is the number of values that has to be created from fft calculation
        zpad = int(8 * self.n / 2)

        # Do fft calculation, and convert results to decibel through dbv function
        decibel = self.dbv(np.fft.ifft(sif, zpad, 1)) 
        
        real_value = decibel[:, 0:int(decibel.shape[1] / 2)]
        max_real = real_value.max() 
        result_data = real_value - max_real

        #### 2 pulse cancelor RTI plot
        sif2 = sif[1:sif.shape[0], :] - sif[:sif.shape[0]-1, :]
        last = sif[-1, :]
        sif2 = np.vstack((sif2, last))
        # print(sif2, sif2.shape, sif.shape, zpad)
        v = np.fft.ifft(sif2, zpad, 1)
        decibel = self.dbv(v)
        real_value = decibel[:, 0:int(decibel.shape[1] / 2)]
        max_real = real_value.max() 
        result_data = real_value - max_real

        print('time, data: ', result_time.shape, result_data.shape)
        # result_time = result_time[:50]
        # result_data = result_data[:50]
        
        # print(result_time.dtype, result_data.dtype)
        return result_time, result_data
