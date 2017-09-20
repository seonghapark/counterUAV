import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors 
from matplotlib import style


style.use('fivethirtyeight')

infile = open("dummy.txt",'r')
color_file = open("color.txt",'r')
color=[]
for i in range(0,80):
	color.append(int(color_file.readline()))

set_t = 100
set_d = 10
calculate = 100/10

fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)


def animate(i):
	global count
	count+=1;
	plt.xlim(count-10,count)
	graph_data = infile.readline()
	datas = graph_data.split()
	for dis in range(0,set_d):
		sharp = '#'+str(hex(color[int(datas[dis])+79]))[2:].zfill(6)
		plt.scatter(count,dis*calculate,c=sharp)


count = -1
#plt.xlim(0,100)
plt.ylim(0,100)
ani = animation.FuncAnimation(fig, animate, interval=1000, frames = set_t-1, repeat = False)
plt.show()