outfile = open("color.txt",'w')

#color = []
color_code = 0xFF0000
for i in range(0,80):
	#color.append(color_code)
	outfile.write(str(color_code))
	outfile.write("\n");
	if(i%5==0):
		color_code-=0x03FFFC
		#color_code-=0x040000
		#color_code+=0x000004
	else:
		color_code-=0x02FFFD
		#color_code-=0x030000
		#color_code+=0x000003
