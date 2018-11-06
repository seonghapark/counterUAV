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
def extract_amp_stats(parent_dir, sub_dirs, file_ext=FILE_EXT, bands=60, frames=41):
        window_size = 128 * (frames - 1)
        labels = []
        amp_med = []
        amp_mean = []
        amp_std = []
        amp_min = []
        amp_max = []
        amp_rge = [] #range (max-min)
        amp_ratio = [] #ratio (max/min)

        for sub_dir in sub_dirs:
            for fn in g.glob(os.path.join(parent_dir, sub_dir, file_ext)):
                Y, sr = librosa.load(fn)
                lbl = fn.split('\\')[2].split('_')[1]
                for (start, end) in windows(Y, window_size):
                        start = int(start)
                        end = int(end)
                        if(len(Y[start:end]) == window_size):
                                amp_med.append(np.median(Y[start:end]))
                                amp_mean.append(np.mean(Y[start:end]))
                                amp_std.append(np.std(Y[start:end]))
                                amp_min.append(np.min(Y[start:end]))
                                amp_max.append(np.max(Y[start:end]))
                                amp_rge.append(np.max(Y[start:end])-np.min(Y[start:end]))
                                amp_ratio.append(np.max(Y[start:end])/np.min(Y[start:end]))
                                labels.append(lbl)

        amp_med = np.asarray(amp_med)
        amp_mean = np.asarray(amp_mean)
        amp_std = np.asarray(amp_std)
        amp_min = np.asarray(amp_min)
        amp_max = np.asarray(amp_max)
        amp_rge = np.asarray(amp_rge)
        amp_ratio = np.asarray(amp_ratio)
        r_amp_med = np.reshape(amp_med, [-1,1])
        r_amp_mean = np.reshape(amp_mean, [-1,1])
        r_amp_std = np.reshape(amp_std, [-1,1])
        r_amp_min = np.reshape(amp_min, [-1,1])
        r_amp_max = np.reshape(amp_max, [-1,1])
        r_amp_rge = np.reshape(amp_rge, [-1,1])
        r_amp_ratio = np.reshape(amp_ratio, [-1,1])
        amp_stat = np.append(r_amp_med, r_amp_mean, axis=1)
        amp_stat = np.append(amp_stat, r_amp_std, axis=1)
        amp_stat = np.append(amp_stat, r_amp_min, axis=1)
        amp_stat = np.append(amp_stat, r_amp_max, axis=1)
        amp_stat = np.append(amp_stat, r_amp_rge, axis=1)
        amp_stat = np.append(amp_stat, r_amp_ratio, axis=1)
        
        #print(amp_stat[0][0])
        #print(np.ndim(amp_stat))
                
        return amp_stat

def extract_diffamp_stats_1(parent_dir, sub_dirs, file_ext=FILE_EXT, bands=60, frames=41):
        window_size = 128 * (frames - 1)
        labels = []
        amp_med = []
        amp_mean = []
        amp_std = []
        amp_min = []
        amp_max = []
        amp_rge = [] #range (max-min)
        amp_ratio = [] #ratio (max/min)

        for sub_dir in sub_dirs:
            for fn in g.glob(os.path.join(parent_dir, sub_dir, file_ext)):
                Y, sr = librosa.load(fn)
                lbl = fn.split('\\')[2].split('_')[1]
                Y = np.gradient(Y)
                for (start, end) in windows(Y, window_size):
                        start = int(start)
                        end = int(end)
                        if(len(Y[start:end]) == window_size):
                                amp_med.append(np.median(Y[start:end]))
                                amp_mean.append(np.mean(Y[start:end]))
                                amp_std.append(np.std(Y[start:end]))
                                amp_min.append(np.min(Y[start:end]))
                                amp_max.append(np.max(Y[start:end]))
                                amp_rge.append(np.max(Y[start:end])-np.min(Y[start:end]))
                                amp_ratio.append(np.max(Y[start:end])/np.min(Y[start:end]))
                                labels.append(lbl)

        amp_med = np.asarray(amp_med)
        amp_mean = np.asarray(amp_mean)
        amp_std = np.asarray(amp_std)
        amp_min = np.asarray(amp_min)
        amp_max = np.asarray(amp_max)
        amp_rge = np.asarray(amp_rge)
        amp_ratio = np.asarray(amp_ratio)
        r_amp_med = np.reshape(amp_med, [-1,1])
        r_amp_mean = np.reshape(amp_mean, [-1,1])
        r_amp_std = np.reshape(amp_std, [-1,1])
        r_amp_min = np.reshape(amp_min, [-1,1])
        r_amp_max = np.reshape(amp_max, [-1,1])
        r_amp_rge = np.reshape(amp_rge, [-1,1])
        r_amp_ratio = np.reshape(amp_ratio, [-1,1])
        diffamp_stat_1 = np.append(r_amp_med, r_amp_mean, axis=1)
        diffamp_stat_1 = np.append(diffamp_stat_1, r_amp_std, axis=1)
        diffamp_stat_1 = np.append(diffamp_stat_1, r_amp_min, axis=1)
        diffamp_stat_1 = np.append(diffamp_stat_1, r_amp_max, axis=1)
        diffamp_stat_1 = np.append(diffamp_stat_1, r_amp_rge, axis=1)
        diffamp_stat_1 = np.append(diffamp_stat_1, r_amp_ratio, axis=1)
        
        #print(diffamp_stat_1[0][0])
        #print(len(diffamp_stat_1))
                
        return diffamp_stat_1

def extract_diffamp_stats_2(parent_dir, sub_dirs, file_ext=FILE_EXT, bands=60, frames=41):
        window_size = 128 * (frames - 1)
        labels = []
        amp_med = []
        amp_mean = []
        amp_std = []
        amp_min = []
        amp_max = []
        amp_rge = [] #range (max-min)
        amp_ratio = [] #ratio (max/min)

        for sub_dir in sub_dirs:
            for fn in g.glob(os.path.join(parent_dir, sub_dir, file_ext)):
                Y, sr = librosa.load(fn)
                lbl = fn.split('\\')[2].split('_')[1]
                Y = np.gradient(Y, 2)
                for (start, end) in windows(Y, window_size):
                        start = int(start)
                        end = int(end)
                        if(len(Y[start:end]) == window_size):
                                amp_med.append(np.median(Y[start:end]))
                                amp_mean.append(np.mean(Y[start:end]))
                                amp_std.append(np.std(Y[start:end]))
                                amp_min.append(np.min(Y[start:end]))
                                amp_max.append(np.max(Y[start:end]))
                                amp_rge.append(np.max(Y[start:end])-np.min(Y[start:end]))
                                amp_ratio.append(np.max(Y[start:end])/np.min(Y[start:end]))
                                labels.append(lbl)

        amp_med = np.asarray(amp_med)
        amp_mean = np.asarray(amp_mean)
        amp_std = np.asarray(amp_std)
        amp_min = np.asarray(amp_min)
        amp_max = np.asarray(amp_max)
        amp_rge = np.asarray(amp_rge)
        amp_ratio = np.asarray(amp_ratio)
        r_amp_med = np.reshape(amp_med, [-1,1])
        r_amp_mean = np.reshape(amp_mean, [-1,1])
        r_amp_std = np.reshape(amp_std, [-1,1])
        r_amp_min = np.reshape(amp_min, [-1,1])
        r_amp_max = np.reshape(amp_max, [-1,1])
        r_amp_rge = np.reshape(amp_rge, [-1,1])
        r_amp_ratio = np.reshape(amp_ratio, [-1,1])
        diffamp_stat_2 = np.append(r_amp_med, r_amp_mean, axis=1)
        diffamp_stat_2 = np.append(diffamp_stat_2, r_amp_std, axis=1)
        diffamp_stat_2 = np.append(diffamp_stat_2, r_amp_min, axis=1)
        diffamp_stat_2 = np.append(diffamp_stat_2, r_amp_max, axis=1)
        diffamp_stat_2 = np.append(diffamp_stat_2, r_amp_rge, axis=1)
        diffamp_stat_2 = np.append(diffamp_stat_2, r_amp_ratio, axis=1)
        
        #print(diffamp_stat_2[0][0])
        #print(len(diffamp_stat_2))
                
        return diffamp_stat_2
    
        
print(extract_diffamp_stats_1('C:/Users/USER/Desktop/counterUAV/experiment_data',sub_dirs))
print(extract_diffamp_stats_2('C:/Users/USER/Desktop/counterUAV/experiment_data',sub_dirs))
