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
        self.path = path
        self.file_paths = g.glob(os.path.join(path, file_ext))
        self.file_names = None  # list of file name
        self.raw_data = None
        self.labels = None  # list of label
    '''
    Read all wav files in directory by filename, label, raw data.
    '''
    def read_wavs(self, intval=False):
        loader = LoadPlot()
        raw_data = loader.load_sound_files(self.file_paths, intval=intval)

        labels = []
        file_names = []

        for p in self.file_paths:
            path, filename = os.path.split(p)
            filename = filename.split('.')[0]   # remove file extension
            freq_labels = filename.split('_')[1]    # extract labels from the file name
            file_names.append(filename)
            labels.append(freq_labels)
        
        print('Length of raw_freq:', len(raw_data), '\nLength of labels', len(labels)) 
        assert len(raw_data) == len(labels)
        assert len(labels) == len(file_names)

        self.raw_data = raw_data
        self.labels = labels
        self.file_names = file_names

    '''
    Write data to wav files.
    It needs to have one-to-one relationship between file_names and data.
    '''
    def write_wavs(self, data,  filenames, sr=5682, ext=".wav", tag=""):
        tag = "_" + tag
        print(len(data), len(filenames))
        assert len(data) == len(filenames)
        for idx in range(len(data)):
            librosa.output.write_wav(
                os.path.join(self.path, filenames[idx].split('.')[0] + tag + ext),
                data[idx],
                sr)

    '''
    iterator that yields name, data, label
    '''
    def files(self):
        i = 0
        print('Length of files:', len(self.file_names))
        while i < len(self.file_names):
            yield self.file_names[i], self.raw_data[i][1], self.raw_data[i][0]
            i += 1

    '''
    filename to label
    '''
    def get_label(self, filename):
        label = filename.split('_')[1]    # extract labels from the file name
        return label

    def chunks(self, y, sr):
        # print("Get Chunk")
        i = 0
        while i < len(y.shape[1]):
            yield y[0, i:i+sr], y[1, i:i+sr]
            i += sr


def main():
    helper = wav_helper(sys.argv[1])
    helper.read_wavs()

    #print('raw_freq: ', helper.raw_freq)
    print('labels: ', helper.labels)
    print('filenames: ', helper.file_names)

if __name__ == "__main__":
    main()
