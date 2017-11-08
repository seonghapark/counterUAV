import numpy as np
import sys
import pylab as pl

from pykalman import KalmanFilter

in_t = open("max_time.txt", "r")
in_maxindex = open("max_distance.txt", "r")
out_t = open("max_time_kf.txt", "w")
out_maxindex = open("max_distance_kf.txt", "w")

data_t = []
data_maxindex = []
data_minindex = []

max_y = 3E8/(2*(2590E6-2260E6))*882/2 
y_val = 1764
ignore_range = int(2.5*y_val/max_y)

wav_time = int(sys.argv[1])
for i in range(0, wav_time):
	split_line = in_t.readline().split()
	split_line = [float (j) for j in split_line]
	data_t = data_t + split_line
	n_time = len(data_t)

	split_line = in_maxindex.readline().split()
	split_line = [float(k) for k in split_line]
	data_maxindex = data_maxindex + split_line

data_t = np.array(data_t)
data_maxindex = np.array(data_maxindex)

kf = KalmanFilter(transition_matrices=np.array([[1, 1], [0, 1]]),
                  transition_covariance=0.01 * np.eye(2))

states_pred = kf.em(data_maxindex).smooth(data_maxindex)[0]

for j in range(0, n_time-1):
	t = (data_t[j]+data_t[j+1])/2
	max_index = np.argmax(data_maxindex[j])
	max_index = (ignore_range*max_y/y_val+max_index*max_y/y_val)
	out_t.write(str(t)+' ')
	out_maxindex.write(str(max_index)+' ')
out_t.write("\n")
out_maxindex.write("\n")