import os
from os.path import isfile, isdir
import numpy as np
import librosa
import librosa.display as display
import librosa.core as core
import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram

PAR_DIR='~/Desktop/counterUAV/raw_data'
labels = ['Others', 'Person', 'Car', 'UAV']

class LoadPlot():
    def __init__(self, i=1, figsize=(12, 4), dpi=200, x=0.5, y=1, fontsize=7):
        self.i = i
        self.figsize = figsize
        self.dpi = dpi
        self.x = x
        self.y = y
        self.fontsize = fontsize

    def load_sound_files(self, path, sr=5862):
        raw_sounds = []

        for fp in path:
            if isfile(fp):
                print('Loading .wav files...')
                Y, sr = librosa.load(fp, sr, mono=False) # Load .wav file as a stereo file (2 channels)
                Y = self.trim_zeros(Y)  # remove zero-values on front
                #print('Value of .wav file:', Y)
                raw_sounds.append(Y)
            else:
                print('Invalid path:', path)

        print('Value of .wav file:', Y)
        print('Shape of .wav file:', np.asarray(Y).shape)
        print('Sync of .wav file:', Y[0], '\nData of .wav file:', Y[1])
        return raw_sounds

    def trim_zeros(self, y):
        assert y.ndim == 2
        sync = y[0]
        data = y[1]

        data = np.trim_zeros(data, 'f')

        # match length of two channel
        d = len(sync) - len(data)
        sync = sync[d:]

        assert len(sync) == len(data)
        _y = np.vstack((sync, data))
        return _y

    def plot_specgram(self, sound_names, raw_sounds):
        i = self.i
        fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        for n, f in zip(sound_names, raw_sounds):
            plt.subplot(len(raw_sounds), 1, i)
            specgram(np.array(f), Fs=5862)
            plt.title(labels[int(n)])
            plt.xlim(0, 100)
            plt.ylim(0, 1000)
            i+=1
        plt.suptitle("Figure 1: Spectrogram", x=self.x, y=self.y, fontsize=self.fontsize)
        plt.tight_layout()
        plt.show()

    def plot_log_specgram(self, sound_names, raw_sounds):
        i = self.i
        fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        for n, f in zip(sound_names, raw_sounds):
            plt.subplot(len(raw_sounds), 1, i)
            D = core.amplitude_to_db(np.abs(librosa.stft(f))**2, ref=np.max)

            display.specshow(D, x_axis='time', y_axis='log')
            plt.title(labels[int(n)])
            plt.xlim(0, 100)
            plt.ylim(0, 1000)
            i+=1

        plt.suptitle("Figure 2: Log-powered spectrogram", x=self.x, y=self.y, fontsize=self.fontsize)
        plt.show()

if __name__ == "__main__":
    #Use only the specified sample data for visualization
    sound_paths = ['20181009_1_100023.wav', '20181009_2_102508.wav']
    sound_names = ['Person', 'Car']

    loader = LoadPlot()
    paths = []
    for i in sound_paths:
        path = '../' + i
        paths.append(path)

    raw_sounds = loader.load_sound_files(paths)
    print('SOUND PATHS:', paths)

    loader.plot_specgram(sound_names, raw_sounds)
    loader.plot_log_specgram(sound_names, raw_sounds)
