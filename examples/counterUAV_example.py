import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy.io import wavfile

# Utility
def dbv(input):
    return 20 * np.log10(abs(input))

fs, data = wavfile.read('range_test2.wav') # range, use ramp signal
# fs, data = wavfile.read('test1HomeAug17.wav')
data = data.T # transpose array "data"
data_len = len(data)
print(data.shape, len(data), data)

rightarray = data[1] # data
leftarray = data[0] # ramp
print(rightarray, leftarray, rightarray.shape, leftarray.shape)

#parse the data here by triggering off rising edge of sync pulse
thresh = 0
start = (leftarray > thresh)
print(start)

Tp = 0.020
n = int(Tp*fs);   # number of samples per pulse
nsif=int(round(data.shape[1]/n)-1)
print(n,round(data.shape[1]/n))
sif=np.zeros([nsif,n], dtype=np.int16)

# print(nsif, sif, n)
# print(start.shape[0]-n)
# print(len(sif[0,:]), n)
print(start.shape[0]-n)
count = 0
time = []
for ii in range(int(fs/2),int((start.shape[0]-int(fs/2)))):
    if (start[ii] == True) & (start[ii-11:ii-1].mean() == 0):
        sif[count,:] = rightarray[ii:ii+n]
        time.append(ii * 1. / fs)
        count = count + 1
print(count)
print(len(time))

time=np.array(time)  
print(len(time))
#Remove no signal part.
sif=sif[:count,:]
print(len(sif))

#remove average.
sif= sif-np.tile(sif.mean(0), [sif.shape[0],1]);
zpad = int(8*n/2)
# print(len(sif), sif)
# # RTI plot
# P.figure();
v=dbv(np.fft.ifft(sif, zpad,1))
print(v.shape)
s=v[:,0:int(v.shape[1]/2)]
# print ('Shape of result: %d' %(s.shape,))
# print(s.shape)
m=s.max()

import pylab as P

c = 3E8
lfm = [2260E6,2590E6]
fstart = lfm[0] #(Hz) LFM start frequency
fstop = lfm[1] #(Hz) LFM stop frequency
BW = fstop-fstart; #(Hz) transmti bandwidth
f = np.linspace(fstart, fstop, int(n/2)) #instantaneous transmit frequency  
rr = c/(2*BW)
max_range = rr*n/2

print(len(time))   
print(np.linspace(0, max_range, int(zpad/2)))   # extent

P.pcolormesh(np.linspace(0, max_range, int(zpad/2)), time, s-m, edgecolors = 'None');
P.plt.gca().invert_yaxis()
# #P.matshow(s[0:time.shape[0]]-m)
P.colorbar();
P.ylabel('time (s)');
P.xlabel('range (m)');
P.title('RTI without clutter rejection');
# P.clim([-80,0])
# P.xlim([0,300])
P.show()
