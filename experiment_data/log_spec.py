import librosa
import os
import numpy as np
import glob as g
from os.path import isfile, isdir

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

        print(len(log_specgrams))
        print(np.ndim(log_specgrams))
        print(len(log_specgrams[0][0]))
        print(log_specgrams[0])
        print(len(log_specgrams[0]))
        log_specgrams = np.asarray(log_specgrams).reshape(len(log_specgrams),bands,frames,1)
        print(np.ndim(log_specgrams))
        features = np.concatenate((log_specgrams, np.zeros(np.shape(log_specgrams))), axis = 3)

        for i in range(len(features)):
            features[i, :, :, 1] = librosa.feature.delta(features[i, :, :, 0])
    
        return 0


print(extract_log_spec('C:/Users/USER/Desktop/counterUAV/experiment_data',sub_dirs))


