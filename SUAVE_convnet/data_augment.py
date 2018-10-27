import librosa
import sys
import glob as g
import os
from os.path import isfile, isdir
import numpy as np

# For augmenting .wav data

FILE_EXT='*.wav'
DATA_PATH='/home/jeonghwan/Desktop/counterUAV/raw_data'
PATH='/home/jeonghwan/Desktop/counterUAV/raw_data/data_process'
sys.path.insert(0, PATH)
from visualize import LoadPlot

class DataAugmentor():
    def __init__(self, file_ext=FILE_EXT):
        opt = {}
        opt['file_ext'] = file_ext

    def freq_shifting(self, path, num_steps=4):
        Y, sr = librosa.load(path, sr=5682)
        # Shift up by a major third (four half-steps)
        Y_shifted = librosa.effects.pitch_shift(Y, sr, num_steps)

        return Y_shifted, sr

#    def visualize

def main():
    # Frequency shift and visualize in log-spectrogram
    loader = LoadPlot()
    paths = []

    file_paths = g.glob(os.path.join(DATA_PATH, FILE_EXT))
    #print('File path:', g.glob(os.path.join(DATA_PATH, FILE_EXT)))

    try:
        loader = LoadPlot()
        raw_freq = loader.load_sound_files(file_paths)

    except IOError:
        print('IOError: Could not find file path')

if __name__ == "__main__":
    main()
