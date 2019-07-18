
# coding: utf-8

# # counterUAV

# In[1]:


# Common imports
import numpy as np
import pandas as pd
import os, sys, glob  
from os.path import isfile, isdir
import librosa
import librosa.display
import librosa.core as core
import scipy.io.wavfile as wavfile
from scipy.fftpack import fft
# To plot pretty figures
import matplotlib
import matplotlib.pyplot as plt
#from scipy.signal import spectrogram
from matplotlib.pyplot import specgram
#get_ipython().run_line_magic('matplotlib', 'inline')


import warnings
warnings.filterwarnings("ignore")   # To rid of warnings 

os_sep = os.sep 

if sys.platform == 'win32':   # if windows 
    home = os.path.join('C:', os.sep, 'Users')      
elif sys.platform == "linux" or sys.platform == "linux2" :    
    home = os.path.expanduser("~")   # home = os.getenv("HOME")

# ### label file
# ####  checking interval

time_list = np.load('time_list.npy', allow_pickle=True)#[[파일 하나],[start, finish],..]
label_list = np.load('label_list.npy', allow_pickle=True)#[person,person,car,dron,..]
#wav_repo = os.path.join(home, '승윤', 'Desktop', 'purdue','연구자료','counterUAV', 'data')
wav_repo = 'C://Users//승윤//Desktop//purdue//연구자료//counterUAV//data'
wav_data = glob.glob(os.path.join(wav_repo,'**','*.wav'), recursive=True)


# In[9]:


print(len(wav_data))


# In[10]:


def trim_zeros(y):#wav 앞부분에 쓸모 없는 부분 자름
        # in mono
        if y.ndim == 1:#데이터만
            _y = np.trim_zeros(y, 'f')#배열에 앞 뒤 여백(0)을 없앰 f의미는 앞에서 부터 자름임
            return _y

        assert y.ndim == 2 #데이터와 싱크 둘다 들어옴
        sync = y[0]
        data = y[1]

        data = np.trim_zeros(data, 'f')#데이터 날림

        # match length of two channel
        d = len(sync) - len(data)
        sync = sync[d:]

        assert len(sync) == len(data)
        _y = np.vstack((sync, data))
        return _y


# #### fft first & cut 

# In[11]:


def plot_specgram(file, i):#i번째 file
    print(file)
    samplingrate=5862
    Y, sr = librosa.load(file, sr=samplingrate, mono=False) # mono=False 이므로 shape(2,~) 형태
    #time = np.linspace(0, len(y)/sr, len(y))#time for wav file
    Y =  trim_zeros(Y)
    Y[1] = fft(Y[1])
    #tmp = np.array([])
    tmp = []
    for timeline in range(0,len(time_list[i])):#i번째 file vaild time list
        time_start_index = time_list[i][timeline][0] * samplingrate
        time_finis_index = time_list[i][timeline][1] * samplingrate
        print("start: ",time_start_index,"finish: ",time_finis_index)
        tmp.extend(Y[1][time_start_index:time_finis_index])
    Y = tmp
    print(len(Y)/samplingrate)
    '''
    plt.figure(figsize=(13, 9), dpi=150)  #창크기, 해상도
    plt.subplot(1, 1, 1) # 그래프를 2행 1열 i번째에 그린다.
    specgram(Y, Fs=samplingrate)
    plt.colorbar()
    plt.title('stereo 1')
    plt.show()
    '''


# In[12]:

'''
for i in range(len(wav_data)) :
    print(wav_data[i].split('\\')[-1])
    plot_specgram(wav_data[i], i)
    print(label_list[i])
'''
# #### cut first & fft

# In[13]:


def plot_specgram_1(file, i):#i번째 file
    print(file)
    samplingrate=5862
    Y, sr = librosa.load(file, sr=samplingrate, mono=False) # mono=False 이므로 shape(2,~) 형태
    Y =  trim_zeros(Y)
    tmp = []
    for timeline in range(0,len(time_list[i])):#i번째 file vaild time list
        time_start_index = time_list[i][timeline][0] * samplingrate
        time_finis_index = time_list[i][timeline][1] * samplingrate
        print("start: ",time_start_index,"finish: ",time_finis_index)
        tmp.extend(Y[1][time_start_index:time_finis_index])
    Y1 = tmp
    print(len(Y1)/samplingrate)
    Y1 = np.array(Y1)
    librosa.output.write_wav('.//after_data//'+str(i+1)+'_'+label_list[i]+".wav", Y1, samplingrate, norm=False)#saved mono
    librosa.output.write_wav('.//after_data_normalize//'+str(i+1)+'_'+label_list[i]+".wav", Y1, samplingrate, norm=1)
    Y1 = fft(Y1)
    '''
    plt.figure(figsize=(13, 9), dpi=150)  #창크기, 해상도
    plt.subplot(1, 1, 1) # 그래프를 2행 1열 i번째에 그린다.
    specgram(Y1, Fs=samplingrate)
    plt.colorbar()
    plt.title('stereo 1')
    plt.show()
    '''

# In[14]:


for i in range(len(wav_data)) :
    print(wav_data[i].split('\\')[-1])
    plot_specgram_1(wav_data[i],i)

# stereo 0 = sync, stereo 1 = data 이므로 input으로는 stereo 1만 사용해도 충분하다고 생각 
