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


wav_repo = 'C://Users//승윤//Desktop//purdue//연구자료//extractwav//cut_wav'
wav_data = glob.glob(os.path.join(wav_repo,'**','*.wav'), recursive=True)

print(len(wav_data))

other_wav = []
person_wav = []
car_wav = []
dron_wav = []

for wav_file in wav_data:
      Y, sr = librosa.load(wav_file, sr=5862, mono=False)
      wav_file = wav_file.split('_')[-1]
      label = wav_file.split('.')[0]
      if label == 'other':
            print('other')
            other_wav.extend(Y)
      elif label == 'person':
            print('person')
            person_wav.extend(Y)
      elif label == 'car':
            print('car')
            car_wav.extend(Y)
      elif label == 'drone':
            print('drone')
            dron_wav.extend(Y)
'''
other_wav = np.array(other_wav)
person_wav = np.array(person_wav)
car_wav = np.array(car_wav)
dron_wav = np.array(dron_wav)
'''

print(len(other_wav))
print(len(person_wav))
print(len(car_wav))
print(len(dron_wav))

time = len(dron_wav)

train_other_time = int(time*4/5)
train_person_time = int(time*4/5)
train_car_time = int(time*4/5)
train_dron_time = int(time*4/5)

print(train_dron_time)

'''
train_other_time = int(len(other_wav)*4/5)
train_person_time = int(len(person_wav)*4/5)
train_car_time = int(len(car_wav)*4/5)
train_dron_time = int(len(dron_wav)*4/5)
'''
push = 5862*

train_other = other_wav[push:train_other_time]
train_person = person_wav[push:train_person_time]
train_car = car_wav[push:train_car_time]
train_dron = dron_wav[0:train_dron_time]

test_other = other_wav[train_other_time + push:-1]
test_person = person_wav[train_person_time + push:-1]
test_car = car_wav[train_car_time + push:-1]
test_dron = dron_wav[train_dron_time:-1]

train_other = np.array(train_other)
train_person = np.array(train_person)
train_car = np.array(train_car)
train_dron = np.array(train_dron)
test_other = np.array(test_other)
test_person = np.array(test_person)
test_car = np.array(test_car)
test_dron = np.array(test_dron)

print(len(train_other))
print(len(train_person))
print(len(train_car))
print(len(train_dron))
print('')
print(len(test_other))
print(len(test_person))
print(len(test_car))
print(len(test_dron))

file_direc = 'C://Users//승윤//Desktop//purdue//연구자료//extractwav//all_wav//training//'
librosa.output.write_wav(file_direc+'other.wav', train_other, 5862, norm=False)
librosa.output.write_wav(file_direc+'person.wav', train_person, 5862, norm=False)
librosa.output.write_wav(file_direc+'car.wav', train_car, 5862, norm=False)
librosa.output.write_wav(file_direc+'drone.wav', train_dron, 5862, norm=False)

file_direc = 'C://Users//승윤//Desktop//purdue//연구자료//extractwav//all_wav//testing//'
librosa.output.write_wav(file_direc+'other.wav', test_other, 5862, norm=False)
librosa.output.write_wav(file_direc+'person.wav', test_person, 5862, norm=False)
librosa.output.write_wav(file_direc+'car.wav', test_car, 5862, norm=False)
librosa.output.write_wav(file_direc+'drone.wav', test_dron, 5862, norm=False)

wav_repo = 'C://Users//승윤//Desktop//purdue//연구자료//extractwav//all_wav//'
wav_data = glob.glob(os.path.join(wav_repo,'**','*.wav'), recursive=True)

plt.figure(figsize=(26, 18), dpi=100)
for i in range(len(wav_data)):
      print(wav_data[i].split('//')[-1])
      wav, sr = librosa.load(wav_data[i], sr=5862, mono=False)
      plt.subplot(4, 1, (i)%4+1) # 그래프를 2행 1열 i번째에 그린다.(0번째 없음)
      specgram(wav, Fs=5862)
      plt.xlabel('Time')
      plt.ylabel('Frequency')
      plt.colorbar()
      plt.title(i)
      if i%4==3:
            plt.xlabel('')
            plt.show()



