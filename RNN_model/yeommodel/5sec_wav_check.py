#!/usr/bin/python
# -*- coding: cp949 -*-


import os

file_dir = 'C://Users//����//Desktop//purdue//�����ڷ�//extractwav//rnn_data02//training//'
#file_dir = 'D://github//UAVgit//counterUAV//RNN_model//yeommodel//5sec_slice_wav_data//'
wav_files = os.listdir(file_dir)
print(len(wav_files))
i=0
for wav_file in wav_files:
      wav_file = file_dir + wav_file
      try:
            n = os.path.getsize(wav_file)
            print(n,'byte', i)
            #print(n / 1024, "KB", i)                       # ų�ι���Ʈ ������
      except os.error:
            print("������ ���ų� �����Դϴ�.")
      i = i+1
