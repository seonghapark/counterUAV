import matplotlib.pyplot as plt
import numpy as np
import sys
import zmq
from scipy.io import wavfile
from scipy.fftpack import fft
from queue import Queue

out_t = open("time_ndarray.txt","w")
out_sm = open("val_ndarray.txt","w")
fs = 44100

class inwav_handler:
	def __init__(self, file_name):
		self.fs, self.data = wavfile.read(file_name)
		self.data = self.data.T
		self.count = 0
	def get_chunk(self):
		if self.count + fs < self.data.shape[1]:
			data = self.data[:, self.count : self.count+fs]
			self.count += fs
			return data
		else:
			return None

class fft_handler:
	def __init__(self):
		self.opp = 0
		self.fs = fs
		self.Tp = 0.020 
		self.n = int(self.Tp*self.fs); 
		self.fsif=np.zeros([10000,self.n], dtype=np.int16)

	def dbv(self, input):
	    return 20 * np.log10(abs(input))

	def get_line(self, raw):
		self.leftarray = raw[0]
		self.rightarray = raw[1]
		thresh = 0
		self.start = (self.leftarray > thresh)

	def data_process(self):
		count = 0
		time = [] # time is a list
		for ii in range(11, int((self.start.shape[0]-self.n))): 
		    if (self.start[ii] == True) & (self.start[ii-11:ii-1].mean() == 0): # if start[ii] is true and the mean of from start[ii-11] to start[ii-1] is zero
		        self.fsif[count,:] = self.rightarray[ii:ii+self.n] # then copy rightarray from ii to ii+n and paste them to sif[count] --> sif[count] is a list
		        time.append((ii + int(self.start.shape[0])*self.opp) * 1. / self.fs) # append time, the time is ii/fs --> few micro seconds (0.0001 sec or so)
		        count = count + 1
		self.opp+=1

		self.time=np.array(time)  # change the format of time from list to to np.array
		sif=self.fsif[:count,:] # truncate sif --> remove all redundant array lists in sif, just in case if sif is longer then count
		sif= sif-np.tile(sif.mean(0), [sif.shape[0],1]);
		zpad = int(8*self.n/2)  # create the number_of_ifft_entities --> which is the number of vales that has to be created from fft calculation
		v=self.dbv(np.fft.ifft(sif, zpad,1)) # Do fft calculation, and convert results to decibel through dbv function
		s=v[:,0:int(v.shape[1]/2)] 
		m=s.max() 
		self.s= s-m
		self.print_result()
		return self.time, self.s

	def print_result(self):

		for k in range(0,len(self.time)):
			out_t.write(str(self.time[k])+' ')
		out_t.write("\n")
		out_t.flush()

		for kk in range(0,self.s.shape[0]):
			for pp in range(0,self.s.shape[1]):
				out_sm.write(str(self.s[kk][pp])+' ')
			out_sm.write("\n")
			out_sm.flush()



def main():
	#inwav part
	print("start inwav part")
	file_name = './'+sys.argv[1]
	inwav = inwav_handler(file_name)
	print("end inwav part")


	#fft part
	print("start fft part")
	fft = fft_handler()
	count = 0
	while(1):
		raw = inwav.get_chunk()
		if raw is None:
			break
		fft.get_line(raw)
		time, result = fft.data_process()
		print("in fft", count, time.shape, result.shape)
		count+=1
	print("end fft part")


main()