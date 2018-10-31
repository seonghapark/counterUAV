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
    def __init__(self, path, file_ext="*.wav"):
        self.file_ext = file_ext
        self.file_paths = g.glob(os.path.join(path, file_ext))
        self.file_names = None  # list of file name
        self.raw_freq = None    # list of raw data
        self.labels = None  # list of label
    '''
    Read all wav files in directory by filename, label, raw data.
    '''
    def read_files(self):
        loader = LoadPlot()
        raw_freq = loader.load_sound_files(self.file_paths)
        labels = []
        file_names = []

        for p in self.file_paths:
            path, filename = os.path.split(p)
            filename = filename.split('.')[0]   # remove file extension
            freq_labels = filename.split('_')[1]    # extract labels from the file name
            file_names.append(filename)
            labels.append(freq_labels)
            
        assert len(raw_freq) == len(labels)
        assert len(labels) == len(file_names)

        self.raw_freq = raw_freq
        self.labels = labels
        self.file_names = file_names

    '''
    iterator that yields name, data, label
    '''
    def files(self):
        i = 0
        while i < len(self.file_names):
            yield self.file_names[i], self.raw_freq[i], self.labels[i]
            i += 1


def main():
    helper = wav_helper(sys.argv[1])
    helper.read_files()

    print('raw_freq: ', helper.raw_freq)
    print('labels: ', helper.labels)
    print('filenames: ', helper.file_names)

if __name__ == "__main__":
    main()
