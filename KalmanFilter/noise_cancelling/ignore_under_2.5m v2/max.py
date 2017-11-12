import numpy as np
import sys

class maxindex_handler:
	def __init__(self):
		self.in_t = open("time_ndarray.txt", "r")
		self.in_val = open("val_ndarray.txt", "r")
		self.out_t = open("time_from_maxindex.txt", "w")
		self.out_distance = open("distance_from_maxindex.txt", "w")

		self.n=882
		self.lfm = [2260E6, 2590E6]
		self.max_detect = 3E8/(2*(self.lfm[1]-self.lfm[0]))*self.n/2 
		self.y_len = 1764

		self.ignore_range = 2.5
		self.ignore_index = int(self.ignore_range*self.y_len/self.max_detect)

	def get_line(self, time):
			self.data_t = []
			self.data_val = []
			split_line = self.in_t.readline().split()
			split_line = [float (j) for j in split_line]
			split_line.append(float(time+1))
			self.data_t = np.array(split_line)
			self.data_tlen = len(self.data_t)

			for j in range (0, self.data_tlen-1):
				split_line = self.in_val.readline().split()
				k=0
				for item in split_line:
					split_line[k] = max(-80,float(item))
					k+=1
				self.data_val.append(split_line)
			self.data_vallen = len(split_line)
			self.data_val = np.array(self.data_val)
			return self.data_tlen, self.data_vallen

	def print_max(self):
		for j in range(0, self.data_tlen-1):
			t = (self.data_t[j]+self.data_t[j+1])/2
			max_index = np.argmax(self.data_val[j][self.ignore_index:])
			ignored = self.ignore_index*self.max_detect/self.y_len
			self.max_range = ignored + max_index*self.max_detect/self.y_len
			self.out_t.write(str(t)+' ')
			self.out_distance.write(str(self.max_range)+' ')
		self.out_t.write("\n")
		self.out_distance.write("\n")

def main():
	print("start get max part")
	maxhandler = maxindex_handler()

	wav_time = int(sys.argv[1])
	for i in range(0, wav_time):
		tlen, vallen = maxhandler.get_line(i)
		print(i,tlen,vallen)
		maxhandler.print_max()
	print("end get max part")
	

main()