import numpy as np
import sys

in_t = open("time_ndarray.txt", "r")
in_val = open("val_ndarray.txt", "r")
out_t = open("mma_time.txt", "w")
out_max = open("max_val.txt","w")
out_maxindex = open("max_index.txt", "w")
out_min = open("min_val.txt", "w")
out_minindex = open("min_index.txt", "w")
out_avg = open("avg_val.txt", "w")

wav_time = int(sys.argv[1])

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
		"""
		k=0
		for item in split_line:
			split_line[k] = max(-80,float(item))
			k+=1
		"""
		split_line = [float(k) for k in split_line]
		data_val.append(split_line)
		n_val = len(split_line)
	data_val = np.array(data_val)

	print("after get input",i,  n_time, n_val)
	if n_val !=0:
		for j in range(0, n_time-1):
			t = (data_t[j]+data_t[j+1])/2
			max_val = np.amax(data_val[j])
			max_index = np.argmax(data_val[j])
			min_val = np.amin(data_val[j])
			min_index = np.argmin(data_val[j])
			avg_val = np.average(data_val[j])

			out_t.write(str(t)+' ')
			out_max.write(str(max_val)+' ')
			out_maxindex.write(str(max_index)+' ')
			out_min.write(str(min_val)+' ')
			out_minindex.write(str(min_index)+' ')
			out_avg.write(str(avg_val)+' ')
		out_t.write("\n")
		out_max.write("\n")
		out_maxindex.write("\n")
		out_min.write("\n")
		out_minindex.write("\n")
		out_avg.write("\n")



