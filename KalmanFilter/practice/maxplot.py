import numpy as np
import sys
import matplotlib.pyplot as plt

in_t = open("max_time_kf.txt", "r")
in_maxindex = open("max_distance_kf.txt", "r")

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

plt.plot(data_t, data_maxindex, 'r')

#obs = plt.plot(data_t, data_maxindex, marker='x', color='b',label='observations')
pred = plt.plot(data_t, data_maxindex, linestyle='-', marker='o', color='r',label='predictions')

plt.show()



