import librosa
import pickle
import sys
import glob as g
import os
from os.path import isfile, isdir
import numpy as np

# For augmenting .wav data

SAMPLE_RATE=5682
FILE_EXT='*.wav'
DATA_PATH='../raw_data/data/'  # path of raw file
AUG_PATH='../raw_data/data/0'
PATH='../raw_data/data_process'  # path for visualize.py
sys.path.insert(0, PATH)
sys.path.insert(0, './')
from visualize import LoadPlot
from wav_helper import wav_helper


"""
This class contains data augmentation methods that increase the size and variance of our dataset.
Data augmentation methods include:

    1) Frequency shifting
    2) Add random noise
    3) Time stretching
    4) Shifting frequency (use np.roll())

All methods should return the following two values:
    1) Y (augmented frequency values)
    2) sr (sampling rate)
"""
class DataAugmentor():
    def __init__(self, file_ext=FILE_EXT):
        opt = {}
        opt['file_ext'] = file_ext
    '''
    This method shifts the signal by n half-steps (n: # of steps)
    '''
    def freq_shifting(self, raw_freq, num_steps=32, sr=SAMPLE_RATE):
    # Shifting frequency values of the signal by <num_setps> * half-steps
    # (i.e. num_steps=32)
        Y = []

        for fr in raw_freq: 
            # Shift up by a major third (four half-steps)
            # Shifting both the data and sync channels
            # Ysync_shifted = librosa.effects.pitch_shift(fr[0], sr, num_steps)
            Ysync_shifted = fr[0]
            Ydata_shifted = librosa.effects.pitch_shift(fr[1], sr, num_steps)
            Y_ps = np.vstack((Ysync_shifted, Ydata_shifted))
            Y.append(Y_ps)
        return Y, sr

    '''
    This method adds random noise to the signal
    '''
    def add_noise(self, raw_freq, scale = 0.05, sr=SAMPLE_RATE):
    # Generate random noise to augment the data
        Yn = []
        length = []
        for i in raw_freq:
            length.append(len(i[1]))
        print("Length:", length)
        
        max_len = max(length) #max value from list
        for i, l in enumerate(length):
            if max_len == l:
                max_len_idx = i

        #print('Max_length_idx:', max_len_idx)
        noise = np.random.uniform(low=2, high=5, size=1) # Generate a random number within a range [low, high] with the length of the longest subarray
        print('Noise value:', noise)
        noise_val = np.full(max_len, noise)
        print('Length of noise list:', len(noise_val))
        for e in raw_freq:
            Ysync = e[0] # Not adding noise to sync channel
            Ydata = e[1] + (noise_val[:len(e[1])] * scale)
            Y = np.vstack((Ysync, Ydata))
            Yn.append(Y)

        return Yn, sr

    '''
    This method streches the data on time axis.
    Parameter raw_freq is a list of data amplitude values (5682 samples * time in seconds)
    It returns a list with time-stretched elements
    '''
    def time_stretching(self, raw_freq, rate=2.0, sr=SAMPLE_RATE):
        Ys = []
        for fr in raw_freq:  # raw_freq has many data files
            # Shifting both the data and sync channels
            Ysync_stretched = librosa.effects.time_stretch(fr[0], rate)
            Ydata_stretched = librosa.effects.time_stretch(fr[1], rate)
            Y = np.vstack((Ysync_stretched, Ydata_stretched))
            Ys.append(Y)

        return Ys, sr

#    def visualize

def main():
    # Frequency shift and visualize in log-spectrogram
    loader = LoadPlot()
    paths = []
    #PICKLE_FILENAME = '1_radar_dataset.pickle'


    file_paths = g.glob(os.path.join(DATA_PATH, FILE_EXT))
    print('File path:', g.glob(os.path.join(DATA_PATH, FILE_EXT)))

    file_names = []
    lbl = []
    for p in file_paths:
        path, filename = os.path.split(p)
        freq_labels = filename.split('_')[1] # extract labels from the file name
        lbl.append(freq_labels)
        file_names.append(filename)
        
    print('Read:', DATA_PATH)        

    """    
    # Pickling data file to reduce the size and speed up load time of the *.wav files
    try:
        if not isfile(PICKLE_FILENAME):
            print(PICKLE_FILENAME, ' not found: Pickling...')

            h_wav = wav_helper(DATA_PATH, file_ext=FILE_EXT)
            h_wav.read_wavs()

            loader = LoadPlot()
            raw_data = h_wav.raw_data

            freq_data = {
                'file_names': file_names,
                'raw_freq': raw_data,
                'labels': lbl
            }

            with open(PICKLE_FILENAME, 'wb') as handle:
                print('Pickling data object...')
                pickle.dump(freq_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

        else:
            print('Loading data from ', PICKLE_FILENAME)
            with open(PICKLE_FILENAME, 'rb') as handle:
                freq_data = pickle.load(handle)

    except IOError:
        print('IOError: Could not find file path')
    """
    print('Read:', DATA_PATH)        
    h_wav = wav_helper(DATA_PATH, file_ext=FILE_EXT)
    h_wav.read_wavs()

    loader = LoadPlot()
    raw_data = h_wav.raw_data

    freq_data = {
        'file_names': file_names,
        'raw_freq': raw_data,
        'labels': lbl
    }


    wavhelp = wav_helper(path=AUG_PATH)
    da = DataAugmentor()
    #freq_data['ps_freq'], sr = da.freq_shifting(freq_data['raw_freq'], num_steps=4)
    #freq_data['ns_freq'], sr = da.add_noise(freq_data['raw_freq'], scale=0.05)
    freq_data['ts_freq'], sr = da.time_stretching(freq_data['raw_freq'],rate=0.5)

    # Write the augmented signals in a .wav file format
    # The tag is in a form of [augmentation method + n_steps]
    # (i.e. ps32 - pitch shifting by 32 half-steps)
    print('Writing augmented data as .wav files...')
    print('FILE NAMES:', file_names)
    #wavhelp.write_wavs(freq_data['ps_freq'], filenames=file_names, tag='ps4')
    #wavhelp.write_wavs(freq_data['ns_freq'], filenames=file_names, tag='ns05')
    wavhelp.write_wavs(freq_data['ts_freq'], filenames=file_names, tag='ts05')

    #d = np.asarray(freq_data['raw_freq'])
    #print('Value of original frequency:', freq_data['raw_freq'], '\nShape of original frequency:', d.shape)
    #print('Value of pitch shifted frequency:', freq_data['ps_freq'][0])
    #print('Value of noise added frequency:', freq_data['ns_freq'][0])
    #print('Value of time stretched frequency:', freq_data['ts_freq'][0])

    '''
    raw = []
    aug = []
    for i, j in zip(freq_data['raw_freq'], freq_data['ns_freq']):
        print('Raw_freq #1~2:', i[1])
        print('Noise_freq #1~2:', j[1])
        raw.append(i[1])
        aug.append(j[1])

    loader.plot_log_specgram(freq_data['labels'][:2], raw[:2]) #visualize in log_spectrogram
    loader.plot_log_specgram(freq_data['labels'][:2], aug[:2])
    '''
if __name__ == "__main__":
    main()
