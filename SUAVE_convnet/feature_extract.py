import librosa
import os
import numpy as np
import glob as g
from os.path import isfile, isdir

FILE_EXT='*.wav'
# Adjust path according to local path settings
PATH='../raw_data'

class FeatureParser():
    def __init__(self, file_ext=FILE_EXT):
        self.file_ext = file_ext

    def windows(self, data, window_size):
        start = 0
        while start < len(data):
            yield start, start + window_size
            start += (window_size / 2)
    '''
    def extract_feature(self, path, pickle_exists=False):
    # Extracting tradition features (i.e. MFCC, chroma) from .wav audio file for Feed-forward neural network
        if pickle_exists is False:
            Y, sample_rate = librosa.load(path)
        else:
            pass

        stft = np.abs(librosa.stft(Y))
        mfcc = np.mean(librosa.feature.mfcc(y=Y, sr=sample_rate, n_mfcc=40).T, axis=0)
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
        mel = np.mean(librosa.feature.melspectrogram(Y, sr=sample_rate).T, axis=0)
        contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)
        tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(Y), sr=sample_rate).T, axis=0)
        return mfcc, chroma, mel, contrast, tonnetz
    '''
    # Extracting and preprocessing features for ConvNet
    def extract_CNNfeature(self, parent_dir, sub_dirs, file_ext=FILE_EXT, bands = 60, frames = 41):
        window_size = 512 * (frames - 1) #Window size = 128
        log_specgrams = []
        labels = []
        if not isfile('radar_CNNdataset.pickle'):
            for label, sub_dir in enumerate(sub_dirs):
                for fn in g.glob(os.path.join(parent_dir, sub_dir, file_ext)):
                    path, filename = os.path.split(fn)
                    lbl = filename.split('_')[1] # extract label from file name
                    #print('LABEL:', lbl)

                    sound_clip, sr = librosa.load(fn)
                    for (start, end) in self.windows(sound_clip, window_size):
                        start = int(start)
                        end = int(end)
                        if(len(sound_clip[start:end]) == window_size):
                            signal = sound_clip[start:end]
                            melspec = librosa.feature.melspectrogram(signal, n_mels = bands)
                            logspec = librosa.core.amplitude_to_db(melspec)
                            logspec = logspec.T.flatten()[:, np.newaxis].T
                            log_specgrams.append(logspec)
                            labels.append(lbl)

            log_specgrams = np.asarray(log_specgrams).reshape(len(log_specgrams), bands, frames, 1)
            features = np.concatenate((log_specgrams, np.zeros(np.shape(log_specgrams))), axis=3)
            for i in range(len(features)):
                features[i, :, :, 1] = librosa.feature.delta(features[i, :, :, 0])
        
        return np.array(features), np.array(labels, dtype=np.int)

    '''
    def parse_audio_files(self, parent_dir, sub_dirs, file_ext=FILE_EXT):
        features, labels = np.empty((2, 5862)), np.empty(0)

        if not isfile('radar_dataset.pickle'):
            for label, sub_dir in enumerate(sub_dirs):
                print('Subdirectory path:{}'.format(sub_dir))
                for fn in g.glob(os.path.join(parent_dir, sub_dir, file_ext)):
                    try:
                        if os.path.exists(fn):
                            mfcc, chroma, mel, contrast, tonnetz = self.extract_feature(fn)
                        else:
                            raise ValueError('Error while extracting feature from the file; at parse_audio_files')
                    except ValueError as err:
                        print(err.args)

                    ext_features = np.hstack([mfcc, chroma, mel, contrast, tonnetz])
                    features = np.vstack([features, ext_features])
                    labels = np.append(labels, fn.split('/')[7].split('-')[1])

        return np.array(features), np.array(labels, dtype = np.int)
    '''

    def k_fold(self, features, labels, k=3, seed=2018):
        k_fold_dict = {}
        assert len(features) == len(labels)
        
        # shuffling the dataset
        np.random.seed(seed)
        idx = np.random.permutation(len(features))
        features, labels = features[idx], labels[idx]

        print(features.shape, labels.shape)

        # make folds
        for i in range(1, k + 1):
            k_fold_dict['fold' + str(i)] = [[], []]

        # counter for each label
        counter = [0] * (len(np.unique(labels)))
        
        # make k_fold_dict
        for feature, label in zip(features, labels):
            n = counter[label] % k + 1
            k_fold_dict['fold' + str(n)][0].append(feature)
            k_fold_dict['fold' + str(n)][1].append(label)
            counter[label] += 1

        return k_fold_dict

    def one_hot_encode(self, labels):
        n_labels = len(labels)
        n_unique_labels = len(np.unique(labels))
        one_hot_encode = np.zeros((n_labels, n_unique_labels))
        one_hot_encode[np.arange(n_labels), labels] = 1
        return one_hot_encode

    # Separating dataset in k-folds for cross validation
    def pick_dataset(self, k_fold_dict, k, idx):
        tr_features = []
        tr_labels = []
        ts_features = []
        ts_labels = []

        for i in range(1, k):
            tag = 'fold'+str(i)
            if i == idx:
                print('set')
                ts_features += k_fold_dict[tag][0]
                ts_labels += k_fold_dict[tag][1]
            else:
                tr_features += k_fold_dict[tag][0]
                tr_labels += k_fold_dict[tag][1]

        return np.array(tr_features), np.array(tr_labels), np.array(ts_features), np.array(ts_labels)


#def main():
    # Sample code for running methods within the current file

'''
if __name__ == '__main__':
    main()
'''
