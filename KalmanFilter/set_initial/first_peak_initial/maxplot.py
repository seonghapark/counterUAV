import numpy as np
import sys
import matplotlib.pyplot as plt

class maxgraph_handler:
	def __init__(self):
		self.in_t = open("time_from_maxindex.txt", "r")
		self.in_distance = open("distance_from_maxindex.txt", "r")

		self.data_t = []
		self.data_maxrange = []

		self.wav_time = int(sys.argv[1])

	def get_line(self):
		for i in range(0, self.wav_time):
			split_line = self.in_t.readline().split()
			split_line = [float (j) for j in split_line]
			self.data_t = np.append(self.data_t, split_line)
			self.data_t = np.array(self.data_t)

			split_line = self.in_distance.readline().split()
			split_line = [float(k) for k in split_line]
			self.data_maxrange = np.append(self.data_maxrange, split_line)
			self.data_maxrange = np.array(self.data_maxrange)

	def draw_graph(self):
		plt.plot(self.data_t, self.data_maxrange, 'r')
		plt.show()

def main():
	print("start maxgraph part")
	maxgraph = maxgraph_handler()
	maxgraph.get_line()
	maxgraph.draw_graph()
	print("end maxgraph part")

main()