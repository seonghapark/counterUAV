import scipy.io.wavfile
import math

rate, data = scipy.io.wavfile.read('20181009_1_100023.wav')

print(rate)
print(data)


print(type(data))
