import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation
from matplotlib.colors import BoundaryNorm

class colorgraph_handler:
	def __init__(self):
		self.n = 882
		self.zpad = 3528
		self.lfm = [2260E6, 2590E6]
		self.max_detect = 3E8/(2*(self.lfm[1]-self.lfm[0]))*self.n/2 
		self.set_t = int(sys.argv[1])

		self.y = np.linspace(0,self.max_detect, int(self.zpad/2))
		self.data_tlen = 0
		self.data_t =np.zeros((300))
		self.data_val = np.zeros((300, self.y.shape[0]))

		self.in_t = open("time_ndarray.txt","r")
		self.in_val = open("val_ndarray.txt","r")

		self.fig = plt.figure()

	def get_line(self, time):
		split_line = self.in_t.readline().split()
		split_line = [float (i) for i in split_line]
		split_line.append(float(time+1))

		self.data_tlen = len(split_line)
		self.data_t = np.array(split_line)

		for val_l in range(0, self.data_tlen-1):
			split_line = self.in_val.readline().split()
			k=0
			for item in split_line:
				split_line[k] = max(-80,float(item))
				k+=1
			self.data_val[val_l] = np.array(split_line)

	def animate_init(self):
		plt.xlabel('Time(s)')
		plt.ylabel('Distance(m)')
		plt.ylim(0,self.max_detect)
		
		self.cmap = plt.get_cmap('jet')
		self.norm = BoundaryNorm([i for i in range(-80,1)], ncolors = self.cmap.N, clip = True)
		plt.pcolormesh(self.data_t, self.y, self.data_val.T, cmap = self.cmap, norm = self.norm)
		plt.colorbar()

	def animate(self, time):
		self.get_line(time)
		plt.pcolormesh(self.data_t, self.y, self.data_val[:self.data_tlen].T, cmap = self.cmap, norm = self.norm)
		plt.xlim(time-self.set_t+1, time+1)

	def draw_graph(self):
		ani = animation.FuncAnimation(self.fig, self.animate, init_func = self.animate_init, interval=1000, frames = self.set_t, repeat = False)
		plt.show()

def main():
	print("start colorgraph part")
	colorgraph = colorgraph_handler()
	colorgraph.draw_graph()
	print("end colorgraph part")


main()