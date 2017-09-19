import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as colors 
import numpy as np
import math

infile = open("input.txt",'r')

#make colorcode array
color = []
color_code = 0xFF0000
for i in range(0,80):
	color.append(color_code)
	if(i%5==0):
		color_code-=0x03FFFC
		#color_code-=0x040000
		#color_code+=0x000004
	else:
		color_code-=0x02FFFD
		#color_code-=0x030000
		#color_code+=0x000003
	
time = 10
distance = 10
calculate = 100/10


plt.figure()

for t in range(0,time):
	s=infile.readline()
	w = s.split()
	for dis in range(0,distance):
		sharp = '#'+str(hex(color[int(w[dis])+79]))[2:].zfill(6)
		plt.scatter(t,dis,c=sharp)

plt.show()