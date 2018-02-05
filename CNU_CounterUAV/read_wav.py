import matplotlib.pyplot as plt
from scipy.io import wavfile

fs, data = wavfile.read('./wav/range_test2.wav')

data = data.T

plt.subplot(2, 1, 1)
plt.plot(range(0, 1124480), data[0])

plt.subplot(2, 1, 2)
plt.plot(range(0, 1124480), data[1])

plt.show()