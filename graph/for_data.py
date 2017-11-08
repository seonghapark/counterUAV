import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy.io import wavfile

out_t = open("time_ndarray.txt","w")
out_sm = open("val_ndarray.txt","w")
infile = open("wav2txt.txt","r")
data = [[],[]]
fs = 44100
Tp = 0.020 
n = int(Tp*fs); 
nsif=int(round(44100/n)-1) 
fsif=np.zeros([10000,n], dtype=np.int16)


# Utility
# Calculate decibel using fft results --> using amplitude of separated signals
def dbv(input):
    return 20 * np.log10(abs(input))



for opp in range(0, 25):
	print(opp)
	line = infile.readline()
	split_line = line.split()
	split_line = [int (i) for i in split_line]
	data[0] = np.array(split_line)
	line = infile.readline()
	split_line = line.split()
	split_line = [int (i) for i in split_line]
	data[1] = np.array(split_line)
	data = np.array(data)

	rightarray = data[1] # data --> signal reflected from object

	leftarray = data[0] # ramp signal --> generated from our radar signal control board


	thresh = 0   # a criterion value for data[0] (leftarray)
	start = (leftarray > thresh) # if values in leftarray > thresh, then true (or false)

	""" to up!!
	Tp = 0.020  # ramp uptime, which is 20 ms --> a factor to analyze sampled data (data[1])
	n = int(Tp*fs);   # number of samples per ramp uptime
	nsif=int(round(data.shape[1]/n)-1) # we'll cut data[1] to n different arrays --> this is the number of array which will be created 

	sif=np.zeros([nsif,n], dtype=np.int16) # Create the same length of arrays with nsif --> after cut the data[1], will put data in sif
	"""


	count = 0
	time = [] # time is a list
	for ii in range(11, int((start.shape[0]-n))): 
	    if (start[ii] == True) & (start[ii-11:ii-1].mean() == 0): # if start[ii] is true and the mean of from start[ii-11] to start[ii-1] is zero
	        fsif[count,:] = rightarray[ii:ii+n] # then copy rightarray from ii to ii+n and paste them to sif[count] --> sif[count] is a list
	        time.append((ii + int(start.shape[0])*opp) * 1. / fs) # append time, the time is ii/fs --> few micro seconds (0.0001 sec or so)
	        count = count + 1


	time=np.array(time)  # change the format of time from list to to np.array

	sif=fsif[:count,:] # truncate sif --> remove all redundant array lists in sif, just in case if sif is longer then count

	sif= sif-np.tile(sif.mean(0), [sif.shape[0],1]);
	zpad = int(8*n/2)  # create the number_of_ifft_entities --> which is the number of vales that has to be created from fft calculation

	v=dbv(np.fft.ifft(sif, zpad,1)) # Do fft calculation, and convert results to decibel through dbv function

	s=v[:,0:int(v.shape[1]/2)] 

	m=s.max() 

	print(time.shape)
	for k in range(0,len(time)):
		out_t.write(str(time[k])+' ')
	out_t.write("\n")
	print((s-m).shape)

	s= s-m
	for kk in range(0,s.shape[0]):
		for pp in range(0,s.shape[1]):
			out_sm.write(str(s[kk][pp])+' ')
		out_sm.write("\n")