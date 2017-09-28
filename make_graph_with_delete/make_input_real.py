import random
import time

outfile = open("dummy.txt",'w')

set_t = 3000
set_d = 1024

now = time.time()+1
for t in range(0,set_t):
	while(time.time()<now):
		1
	now = time.time()+1
	for dis in range(0,set_d):
		outfile.write(str(random.randrange(-79,1)))
		outfile.write(" ")
	outfile.write("\n")
	outfile.flush()