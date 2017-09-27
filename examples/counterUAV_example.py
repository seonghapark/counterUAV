import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy.io import wavfile

# Utility
# Calculate decibel using fft results --> using amplitude of separated signals
def dbv(input):
    return 20 * np.log10(abs(input))

# Read wav file --> result of the reading if sampling rate (fs) and reading values (data)
fs, data = wavfile.read('range_test2.wav') # range, use ramp signal
# fs, data = wavfile.read('test1HomeAug17.wav')
data = data.T # transpose array "data"
data_len = len(data) # data length
print(data.shape, len(data), data)

rightarray = data[1] # data --> signal reflected from object
# Transmitted signal from radar hit on an object/objects and come back to radar (antenna)
# data[1] is the signal reflected and received through our receiver antenna
leftarray = data[0] # ramp signal --> generated from our radar signal control board
print(rightarray, leftarray, rightarray.shape, leftarray.shape)

#parse the data here by triggering off rising edge of sync pulse
thresh = 0   # a criterion value for data[0] (leftarray)
start = (leftarray > thresh) # if values in leftarray > thresh, then true (or false)
print(start)

Tp = 0.020  # ramp uptime, which is 20 ms --> a factor to analyze sampled data (data[1])
n = int(Tp*fs);   # number of samples per ramp uptime
nsif=int(round(data.shape[1]/n)-1) # we'll cut data[1] to n different arrays --> this is the number of array which will be created 
print(n,round(data.shape[1]/n))
sif=np.zeros([nsif,n], dtype=np.int16) # Create the same length of arrays with nsif --> after cut the data[1], will put data in sif
# This array is array of lists, so sif will become n x nsif array

# print(nsif, sif, n)
# print(start.shape[0]-n)
# print(len(sif[0,:]), n)
print(start.shape[0]-n)
count = 0
time = [] # time is a list
for ii in range(int(fs/2),int((start.shape[0]-int(fs/2)))):  # For the length of from fs/2 to the length of data[1]-fs/2
    if (start[ii] == True) & (start[ii-11:ii-1].mean() == 0): # if start[ii] is true and the mean of from start[ii-11] to start[ii-1] is zero
        sif[count,:] = rightarray[ii:ii+n] # then copy rightarray from ii to ii+n and paste them to sif[count] --> sif[count] is a list
        time.append(ii * 1. / fs) # append time, the time is ii/fs --> few micro seconds (0.0001 sec or so)
        count = count + 1
print(count)
print(len(time))

time=np.array(time)  # change the format of time from list to to np.array
print(len(time))
#Remove no signal part.
sif=sif[:count,:] # truncate sif --> remove all redundant array lists in sif, just in case if sif is longer then count
print(len(sif))

#remove average.
sif= sif-np.tile(sif.mean(0), [sif.shape[0],1]);
zpad = int(8*n/2)  # create the number_of_ifft_entities --> which is the number of vales that has to be created from fft calculation
# print(len(sif), sif)
# # RTI plot
# P.figure();
v=dbv(np.fft.ifft(sif, zpad,1)) # Do fft calculation, and convert results to decibel through dbv function
print(v.shape)
s=v[:,0:int(v.shape[1]/2)] # v contains all real and imaginary values (e.g. x and y in x+yi), but we don't need imaginary values so cut them out 
# print ('Shape of result: %d' %(s.shape,))
# print(s.shape)
m=s.max() # get the max value of s

import pylab as P

c = 3E8  # speed of light
lfm = [2260E6,2590E6] # frequency range of transmission signal
fstart = lfm[0] #(Hz) LFM start frequency --> min frequency
fstop = lfm[1] #(Hz) LFM stop frequency --> max frequency
BW = fstop-fstart; #(Hz) transmti bandwidth --> gap between min and max frequency
f = np.linspace(fstart, fstop, int(n/2)) # instantaneous transmit frequency --> create frequency domain (x axis) 
rr = c/(2*BW) # ratio of bandwidth and speed of light
max_range = rr*n/2 # max range which we can see using this radar is determined by rr and the number of sampling per pulse

print(len(time))   
print(np.linspace(0, max_range, int(zpad/2)))   # extent --> just for check, print the values

P.pcolormesh(np.linspace(0, max_range, int(zpad/2)), time, s-m, edgecolors = 'None'); # plot the data using pcolormesh
P.plt.gca().invert_yaxis()
# #P.matshow(s[0:time.shape[0]]-m)
P.colorbar();
P.ylabel('time (s)');
P.xlabel('range (m)');
P.title('RTI without clutter rejection');
# P.clim([-80,0])
# P.xlim([0,300])
P.show()
