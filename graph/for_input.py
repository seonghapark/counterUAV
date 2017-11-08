import numpy as np
from scipy.io import wavfile

outfile = open("wav2txt.txt","w")

fs, data = wavfile.read('range_test2.wav')

data = data.T

#print(data)

count = 1
while (count+44100<len(data[1])):
	for i in range(0, 2):
		for j in range(count, count+44100):
			#print(i,j)
			outfile.write(str(data[i][j])+' ')
		outfile.write("\n")
	count+=44100