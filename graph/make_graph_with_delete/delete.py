import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation
from matplotlib.colors import BoundaryNorm

#global variables
dt = 1
dy = 1
max_t = 100
max_y = 1024
set_t = 3000
fig = plt.figure()

data = np.zeros((max_t,max_y)) #define and initialize data to 0

infile = open("dummy.txt",'r') #input data file

#color setting for pcolormesh
cmap = plt.get_cmap('jet')
norm = BoundaryNorm([i for i in range(-80,1)], ncolors = cmap.N, clip = True)
extent = ((-max_t,0,0,max_y))
im = plt.imshow(data.T,cmap = cmap, norm=norm, animated=True, extent = extent, aspect = 'auto')
fig.colorbar(im)

def init():
	return

def animate(time):
	global data

	#get data from inputfile and make numpy array
	line = infile.readline()
	split_line = line.split()
	split_line = [int (i) for i in split_line]
	split_line = np.array(split_line)

	#delete oldest one and insert new one
	data = np.delete(data,0,0)
	data = np.insert(data, max_t-1, split_line,0)

	#draw_graph
	if(time<max_t):
		im.set_array(data[max_t-1-time:].T)
		im.set_extent((0,time+1,0,max_y))
	else:
		im.set_array(data.T)
		im.set_extent((time-max_t+1,time+1,0,max_y))
	plt.xlim(time-max_t+1,time+1)

	return im,



plt.xlabel('Time(s)')
plt.ylabel('Distance(m)')
plt.ylim(0,max_y)

ani = animation.FuncAnimation(fig, animate, init_func = init, interval=1000, frames = set_t-1, repeat = False)

plt.show()
