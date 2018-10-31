import librosa
import os
import sys
import numpy as np
import glob as g
from os.path import isfile, isdir

PATH = '../raw_data/data_process'  # path for visualize.py
sys.path.insert(0, PATH)
from visualize import LoadPlot


class wav_helper():
    def __init__(self, path, file_ext='*.wav'):
        self.file_ext = file_ext
        self.file_paths = g.glob(os.path.join(path, file_ext))
        self.file_names = []
        self.raw_freq = None
        self.labels = None

    def read_files(self):
        loader = LoadPlot()
        raw_freq = loader.load_sound_files(self.file_paths)
        labels = []

        for p in self.file_paths:
            path, filename = os.path.split(p)
            freq_labels = filename.split('_')[1]    # extract labels from the file name
            self.file_names.append(filename)
            labels.append(freq_labels)
                
        self.raw_freq = raw_freq
        self.labels = labels


def main():
    helper = WavHelper(sys.argv[1])
    helper.read_files()

    print('raw_freq: ', helper.raw_freq)
    print('labels: ', helper.labels)
    print('filenames: ', helper.file_names)

if __name__ == "__main__":
    main()
