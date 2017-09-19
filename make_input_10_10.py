import random

outfile = open("input.txt",'w')

time = 10
distance = 10

for t in range(0,time):
	for dis in range(0,distance):
		outfile.write(str(random.randrange(-79,1)))
		outfile.write(" ")
	outfile.write("\n")