import numpy as np
import sys
import matplotlib.pyplot as plt

in_t = open("mma_time.txt", "r")
in_maxindex = open("max_index.txt", "r")
in_minindex = open("min_index.txt", "r")

data_t = []
data_maxindex = []
data_minindex = []

fig, ax = plt.subplots()
wav_time = int(sys.argv[1])
for i in range(0, wav_time):
	split_line = in_t.readline().split()
	split_line = [float (j) for j in split_line]
	data_t = data_t + split_line
	n_time = len(data_t)

	split_line = in_maxindex.readline().split()
	split_line = [float (k)*200/1738 for k in split_line]
	data_maxindex = data_maxindex + split_line
	split_line = in_minindex.readline().split()
	split_line = [float (k)*200/1738 for k in split_line]
	data_minindex = data_minindex + split_line
	n_val = len(data_minindex)

data_t = np.array(data_t)
data_maxindex = np.array(data_maxindex)
data_minindex = np.array(data_minindex)

ax.plot(data_t, data_maxindex, 'b', label = 'max')
ax.plot(data_t, data_minindex, 'r', label = 'min')
ax.legend()


plt.show()



