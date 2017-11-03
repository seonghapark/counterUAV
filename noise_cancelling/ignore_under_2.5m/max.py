import numpy as np
import sys

in_t = open("time_ndarray.txt", "r")
in_val = open("val_ndarray.txt", "r")
out_t = open("mma_time.txt", "w")
out_maxindex = open("max_index.txt", "w")

wav_time = int(sys.argv[1])

max_y = 3E8/(2*(2590E6-2260E6))*882/2 
y_val = 1764

ignore = int(2.5*y_val/max_y)

for i in range (0, wav_time-1):
	data_t = []
	data_val = []
	split_line = in_t.readline().split()
	split_line = [float (j) for j in split_line]
	split_line.append(float(i+1))
	data_t = np.array(split_line)
	n_time = len(data_t)

	for j in range (0, n_time):
		split_line = in_val.readline().split()
		split_line = split_line[ignore:]
		split_line = [float(k) for k in split_line]
		data_val.append(split_line)
		n_val = len(split_line)
	data_val = np.array(data_val)

	print("after get input",i,  n_time, n_val)
	if n_val !=0:
		for j in range(0, n_time-1):
			t = (data_t[j]+data_t[j+1])/2
			max_index = np.argmax(data_val[j])

			out_t.write(str(t)+' ')
			out_maxindex.write(str(max_index)+' ')
		out_t.write("\n")
		out_maxindex.write("\n")
	



