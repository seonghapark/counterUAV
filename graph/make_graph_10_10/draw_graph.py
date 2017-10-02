import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as colors 
import numpy as np
import math

infile = open("dummy.txt",'r')
color_file = open("color.txt",'r')
color=[]
for i in range(0,80):
	color.append(int(color_file.readline()))
	
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