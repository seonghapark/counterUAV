#using s-m and time ndarray 
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation
from matplotlib.colors import BoundaryNorm

#global variables
n = 882
zpad = 3528
set_t = int(sys.argv[1])
max_y = 3E8/(2*(2590E6-2260E6))*n/2 
y = np.linspace(0,max_y, int(zpad/2)+1)

data_tlen = 0
data_t =np.zeros((200))
data_val = np.zeros((200, y.shape[0]-1))

#file
in_t = open("time_ndarray.txt","r")
in_val = open("val_ndarray.txt","r")

#for graph setting
fig = plt.figure()
cmap = plt.get_cmap('jet')
norm = BoundaryNorm([i for i in range(-80,1)], ncolors = cmap.N, clip = True)
plt.xlabel('Time(s)')
plt.ylabel('Distance(m)')
plt.ylim(0,max_y)


def init():
	plt.pcolormesh(data_t, y, data_val.T, cmap = cmap, norm = norm)
	plt.colorbar()
	return

def get_line(time):
	global data_tlen, data_t, data_val
	split_line = in_t.readline().split()
	split_line = [float (i) for i in split_line]
	split_line.append(float(time+1))

	data_tlen = len(split_line)
	data_t = np.array(split_line)

	for val_l in range(0, data_tlen-1):
		split_line = in_val.readline().split()
		k=0
		for item in split_line:
			split_line[k] = max(-80,float(item))
			k+=1
		data_val[val_l] = np.array(split_line)

def animate(time):
	global data_tlen, data_t, data_val
	get_line(time)
	plt.pcolormesh(data_t, y, data_val[:data_tlen].T, cmap = cmap, norm = norm)
	plt.xlim(time-set_t+1, time+1)

ani = animation.FuncAnimation(fig, animate, init_func = init, interval=1000, frames = set_t, repeat = False)

plt.show()
