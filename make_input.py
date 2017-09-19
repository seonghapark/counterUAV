import random

outfile = open("input.txt",'w')

time = 100
distance = 1024

for t in range(0,time):
	for dis in range(0,distance):
		outfile.write(str(random.randrange(-80,1)))
		outfile.write(" ")
	outfile.write("\n")