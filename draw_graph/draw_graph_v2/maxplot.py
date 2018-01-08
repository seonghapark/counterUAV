import numpy as np
import sys
import matplotlib.pyplot as plt

in_t = open("mma_time.txt", "r")
in_maxindex = open("max_index.txt", "r")

data_t = []
data_maxindex = []
data_minindex = []

wav_time = int(sys.argv[1])
for i in range(0, wav_time):
	split_line = in_t.readline().split()
	split_line = [float (j) for j in split_line]
	data_t = data_t + split_line
	n_time = len(data_t)

	split_line = in_maxindex.readline().split()
	split_line = [float (k)*200/1738 for k in split_line]
	data_maxindex = data_maxindex + split_line


data_t = np.array(data_t)
data_maxindex = np.array(data_maxindex)

plt.plot(data_t, data_maxindex, 'b')


plt.show()



