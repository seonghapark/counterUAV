import librosa
import pickle
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

    def freq_shifting(self, raw_freq, num_steps=4, sr=5682):
        Ys, fs = [], []

        for fr in raw_freq: 
            # Shift up by a major third (four half-steps)
            Y_shifted = librosa.effects.pitch_shift(fr, sr, num_steps)
            Ys.append(Y_shifted)
            fs.append(sr)

        return Ys, sr

#    def visualize

def main():
    # Frequency shift and visualize in log-spectrogram
    loader = LoadPlot()
    paths = []

    file_paths = g.glob(os.path.join(DATA_PATH, FILE_EXT))
    print('File path:', g.glob(os.path.join(DATA_PATH, FILE_EXT)))

    try:
        if not isfile('radar_dataset.pickle'):
            print('radar_dataset.pickle not found: Pickling...')
            loader = LoadPlot()
            raw_freq = loader.load_sound_files(file_paths)

            lbl = []
            for p in file_paths:
                freq_labels= p.split('/')[6].split('_')[1] # extract labels from the file name
                lbl.append(freq_labels)

            freq_data = {'raw_freq': raw_freq,
                    'labels': lbl}

            with open('radar_dataset.pickle', 'wb') as handle:
                print('Pickling data object...')
                pickle.dump(freq_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

        else:
            print('Loading data from radar_dataset.pickle')
            with open('radar_dataset.pickle', 'rb') as handle:
                freq_data = pickle.load(handle)

    except IOError:
        print('IOError: Could not find file path')

    da = DataAugmentor()
    freq_data['ps_freq'], sr = da.freq_shifting(freq_data['raw_freq'])

    loader.plot_specgram(freq_data['labels'][:2], freq_data['raw_freq'][:2])
    loader.plot_specgram(freq_data['labels'][:2], freq_data['ps_freq'][:2])
    #loader.plot_log_specgram(lbl, raw_freq) 

if __name__ == "__main__":
    main()
