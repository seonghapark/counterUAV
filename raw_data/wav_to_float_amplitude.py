import librosa
import numpy as np

Y, sr = librosa.load('20181009_1_100023.wav',sr=None, mono=False)
X, sr = librosa.load('20181009_1_100023.wav',sr=None)
d = librosa.get_duration(Y,sr)
rge = np.max(Y) - np.min(Y)
ratio = np.max(Y)/np.min(Y)

print(Y[1])
