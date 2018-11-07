import librosa
import os
import numpy as np
import glob as g
from os.path import isfile, isdir
import time

start_time = time.time()

FILE_EXT='*.wav'

sub_dirs = []
for i in range(1,3):
        num = str(i)
        sub_dirs.append('fold' + num)

def windows(data, window_size):
        start = 0
        while start < len(data):
            yield start, start + window_size
            start += (window_size / 2)

#statistics of amplitude data
def extract_log_spec (parent_dir, sub_dirs, file_ext=FILE_EXT, bands=60, frames=41):
        window_size = 512 * (frames - 1)
        log_specgrams = []
        labels = []

        for l, sub_dir in enumerate(sub_dirs):
            for fn in g.glob(os.path.join(parent_dir, sub_dir, file_ext)):
                Y,s = librosa.load(fn)
                lbl = fn.split('\\')[2].split('_')[1]
                for (start,end) in windows(Y,window_size):
                    start = int(start)
                    end = int(end)
                    if(len(Y[start:end]) == window_size):
                        signal = Y[start:end]
                        melspec = librosa.feature.melspectrogram(signal, n_mels = bands)
                        logspec = librosa.core.amplitude_to_db(melspec)
                        logspec = logspec.T.flatten()[:, np.newaxis].T
                        log_specgrams.append(logspec)
                        labels.append(lbl)

        log_specgrams = np.asarray(log_specgrams).reshape(len(log_specgrams),bands,frames,1)
        features = np.concatenate((log_specgrams, np.zeros(np.shape(log_specgrams))), axis = 3)

        for i in range(len(features)):
            features[i, :, :, 1] = librosa.feature.delta(features[i, :, :, 0])
    
        return np.array(features), np.array(labels,dtype = np.int)

def one_hot_encode(labels):
    n_labels = len(labels)
    n_unique_labels = len(np.unique(labels))
    one_hot_encode = np.zeros((n_labels,n_unique_labels))
    one_hot_encode[np.arange(n_labels), labels] = 1
    return one_hot_encode




