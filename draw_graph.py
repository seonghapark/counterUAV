import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation
from matplotlib.colors import BoundaryNorm

#global variables
dt = 1
dy = 1
max_t = 10
max_y = 10
set_t = 100
fig = plt.figure() 
ax0 = fig.add_subplot(1,1,1)
bar = False

y = np.mgrid[slice(0, max_y+dy, dy)] #distance numpy array

data = np.zeros((max_t,max_y)) #define and initialize data to 0

#color setting for pcolormesh
cmap = plt.get_cmap('jet')
norm = BoundaryNorm([i for i in range(-80,1)], ncolors = cmap.N, clip = True)

infile = open("dummy.txt",'r') #input data file



def animate(time):
	global data
	global bar
	#get data from inputfile and make numpy array
	line = infile.readline()
	split_line = line.split()
	split_line = [int (i) for i in split_line]
	split_line = np.array(split_line)

	#delete oldest one and insert new one
	data = np.delete(data,0,0)
	data = np.insert(data, max_t-1, split_line,0)

	#print(data)

	#drawing graph
	plt.xlim(time-max_t,time) #fix x_scale
	t=[time,time+1]
	#print(data[-1:])
	im = ax0.pcolormesh(t,y, data[-1:].T, cmap = cmap, norm = norm)
	if(not bar):
		fig.colorbar(im)
		bar = True


plt.xlabel('Time(s)')
plt.ylabel('Distance(m)')
plt.ylim(0,10)

ani = animation.FuncAnimation(fig, animate, interval=1000, frames = set_t-1, repeat = False)

plt.show()
