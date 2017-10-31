import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation
from matplotlib.colors import BoundaryNorm


#using s-m and time ndarray 

#same value 
n = 882
zpad = 3528

#global variables
dt = 1
dy = 1
bar = False
max_t = 25
set_t = 25
max_y = 3E8/(2*(2590E6-2260E6))*n/2 # max range which we can see using this radar is determined by rr and the number of sampling per pulse
y = np.linspace(0,max_y, int(zpad/2)+1)
data_tlen = np.zeros((max_t)) #define and initialize data to 0
data_t = np.zeros((max_t, 100))
data_val = np.zeros((max_t, 100, y.shape[0]-1))

in_t = open("time_ndarray.txt","r")
in_val = open("val_ndarray.txt","r")

fig = plt.figure()
ax0 = fig.add_subplot(1,1,1)
cmap = plt.get_cmap('jet')
norm = BoundaryNorm([i for i in range(-80,1)], ncolors = cmap.N, clip = True)
#extent = ((-max_t,0,0,max_y))
#im = plt.imshow(data.T,cmap = cmap, norm=norm, animated=True, extent = extent, aspect = 'auto')
#fig.colorbar(im)

def init():
	return

def animate(time):
	global data_tlen, data_t, data_val
	global bar
	#get data from inputfile and make numpy array
	split_line = in_t.readline().split()
	split_line = [float (i) for i in split_line]
	#split_line.insert(0,float(time))
	split_line.append(float(time+1))
	data_tlen = np.delete(data_tlen, 0, 0)
	data_tlen = np.insert(data_tlen, max_t-1, len(split_line), 0)
	split_line = np.pad(np.array(split_line), (0, 100 - int(data_tlen[max_t-1])), 'constant')
	data_t = np.delete(data_t, 0, 0)
	data_t = np.insert(data_t, max_t-1, split_line, 0)  #last 0 means axis = xaxis
	data_val = np.delete(data_val, 0, 0)
	data_val = np.insert(data_val, max_t-1, np.zeros((100, y.shape[0]-1)),0)
	for val_l in range(0, int(data_tlen[max_t-1])-1):
		split_line = in_val.readline().split()
		k=0
		for item in split_line:
			split_line[k] = max(-80,float(item))
			k+=1
		split_line = np.array(split_line)
		data_val[max_t-1][val_l]=split_line

	#draw_graph
	"""
	if(time<max_t):
		im.set_array(data[max_t-1-time:].T)
		im.set_extent((0,time+1,0,max_y))
	else:
		im.set_array(data.T)
		im.set_extent((time-max_t+1,time+1,0,max_y))
	plt.xlim(time-max_t+1,time+1)
	"""
	#print(data_t[max_t-1][0:int(data_tlen[max_t-1])])
	#print( data_val[max_t-1][0:int(data_tlen[max_t-1])-1].T)
	im = ax0.pcolormesh(data_t[max_t-1][0:int(data_tlen[max_t-1])], y, data_val[max_t-1][0:int(data_tlen[max_t-1])-1].T, cmap = cmap, norm = norm)
	plt.xlim(time-max_t+1, time+1)

	if(not bar):
		fig.colorbar(im)
		bar = True

	#return im,



plt.xlabel('Time(s)')
plt.ylabel('Distance(m)')
plt.ylim(0,max_y)

ani = animation.FuncAnimation(fig, animate, init_func = init, interval=1000, frames = set_t, repeat = False) #frames = set_t-1

plt.show()
