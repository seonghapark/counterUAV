import zmq
from scipy.io import wavfile
import numpy as np
import sys
from scipy import sparse

fs = 44100


class inwav_handler:
    def __init__(self, file_name):
        self.fs, self.data = wavfile.read(file_name)
        self.data = self.data.T
        self.count = 0

    def get_chunk(self):
        if self.count + fs < self.data.shape[1]:
            data = self.data[:, self.count: self.count + fs]
            self.count += fs
            return data
        else:
            return None


class fft_handler:
    def __init__(self):
        self.opp = 0
        self.fs = fs
        self.Tp = 0.020
        self.n = int(self.Tp * self.fs);
        self.fsif = np.zeros([10000, self.n], dtype=np.int16)

        self.out_t = open("time_ndarray.txt", "w")
        self.out_sm = open("val_ndarray.txt", "w")

    def dbv(self, input):
        return 20 * np.log10(abs(input))

    def get_line(self, raw):
        self.leftarray = raw[0]
        self.rightarray = raw[1]
        thresh = 0
        self.start = (self.leftarray > thresh)

    def data_process(self):
        count = 0
        time = []  # time is a list
        for ii in range(11, int((self.start.shape[0] - self.n))):
            if (self.start[ii] == True) & (self.start[
                                           ii - 11:ii - 1].mean() == 0):  # if start[ii] is true and the mean of from start[ii-11] to start[ii-1] is zero
                self.fsif[count, :] = self.rightarray[
                                      ii:ii + self.n]  # then copy rightarray from ii to ii+n and paste them to sif[count] --> sif[count] is a list
                time.append((ii + int(self.start.shape[
                                          0]) * self.opp) * 1. / self.fs)  # append time, the time is ii/fs --> few micro seconds (0.0001 sec or so)
                count = count + 1
        self.opp += 1
        return time, self.fsif, count


def main():
    # inwav part
    print("start inwav part")
    file_name = './range_test2.wav'
    inwav = inwav_handler(file_name)
    print("end inwav part")

    # fft part
    print("start fft part")
    fft = fft_handler()
    count_fft = 0

    # zmq send context
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:8887")

    print("make zmq context and start send")


    while (1):
        raw = inwav.get_chunk()
        if raw is None:
            break
        fft.get_line(raw)
        time, fsif, count = fft.data_process()

        time_array = np.zeros((count,1), dtype=np.int16) #time list to array

        new_f = fsif[:count][:] #fsif transrate to countx882 array

        for i in range (0,count): # time copy to time_array
            time_array[i][0] = time[i]


        data_array = np.concatenate((new_f,time_array),1) # make send data_array

        print(np.shape(data_array))
        print(data_array)

        print((data_array.ravel()).tobytes())

        socket.send(data_array.ravel()) # send data_array

        print("in fft", count_fft)

        count_fft = count_fft + 1

    print("send : end")


main()