
# coding: utf-8

# In[1]:


import os
import numpy as np
import tensorflow as tf
import random

# In[2]:


path_dir = 'C://Users//승윤//Desktop//purdue//연구자료//counterUAV//raw_data//data_process//data' 
file_list = os.listdir(path_dir)
'''
# 20181016_135027_binary.txt 삭제 (no data)


# In[3]:


print(file_list)


# In[4]:


len(file_list)


# In[5]:


def parse(raw_data):
    data = bytearray(raw_data)
       # print(len(data))
       # parse the sync and data signal in bytearray
    if len(data) < 2:
        return None, None
    if (data[0] >> 6) > 0: # '11'로 시작하는 데이터 일 때, 맨 앞의 데이터 삭제
        del data[:1] #0번 인덱스에 있는 데이터 빼는 코드
    if len(data) % 2 == 1: # 전체 데이터 개수가 홀수인 경우
        del data[-1]  #뒤에 하나 뺌

    values = []
    sync = []
    for index in range(0, len(data), 2): # 0~len(data), 2씩 증가
        if (data[index] >> 6) > 0 and index+2 <len(data): #내가 추가한 코드 
            #first byte에 A 부분이 true일 경우 && data길이가 index+2를 넘는 경우
            index_2 = index + 1 #다음 index로 
        else:
            index_2 = index #아니면 덮어 씌우기
        high = data[index_2] & 0x1F #high = first bytes
        low = data[index_2 + 1] & 0x1F #low = second bytes
        values.append(high << 5 | low) #high BBBBB low CCCCC
        sync.append(True if (data[index_2] >> 5) == 1 else False) #high A 1=true 0=false

    sync = sync #sync = np.array(sync)
    data = values #data = np.array(values)
        
    # print(self.sync, self.data, len(self.sync), len(self.data))
    return sync, data


# In[6]:

sync_list = [] # 모든 파일들의 싱크 정보 리스트
data_list = [] # 모든 파일들의 데이터 정보 리스트
print('raw data - > data list, sync list')
for i in range(len(file_list) - 1):
    src_path = path_dir + '/' + file_list[i]
    data_file = open(src_path, "rb")
    read_data = data_file.read()
    sync, data = parse(read_data)
    sync_list.append(sync)
    data_list.append(data)
    print(i + 1, '번째 파일 완료')

# In[7]:


for index in range(len(file_list) - 1):
    print(index+1, 'True count:', sync_list[index].count(True))
    print(index+1, 'False count:', sync_list[index].count(False))
    print("")


# In[8]:


#len(data_list[4])


# In[9]:


data_list_seconds = [] # 모든 파일들의 데이터 정보(초단위)
file_name = 'data_list_sec'
for i in range(len(file_list) - 1):
    sync = sync_list[i]
    data = data_list[i]

    true_data  = []
    temp_d = []
    count = 0
    for index, tf_value in enumerate(sync):
        if tf_value == True:
            count += 1
            temp_d.append(data[index])#True sync 만 5682개 모여야 1초가 됨
            #F도 해당 시간에 들어온 정보라 세줘야할거 같은데 그냥 빼고 생각하기로 
            if count == 2931:#BBBBBCCCCC를 1로 세니 5682 / 2 만큼 세야 1초
                true_data.append(temp_d)
                count = 0
                temp_d = []
    #fp.write(format(true_data))
    data_list_seconds.append(true_data)
    
    print(i + 1, '번째 파일 길이:' ,len(data_list_seconds[i]),'초', end='')
    print(' ('+file_list[i]+')')
    a = np.array(data_list_seconds)
    print(a.shape)
    
np.save(file_name, a)
    
#앞의 리스트는 프리해줘도 좋음
sync = []
data = []
#안됨 "전구간" 시간 초가 data_list_seconds에 있어서 다 프리는 불가 

# In[10]:

#print(len(data_list_seconds[0]))

# In[11]:


label_path_dir = path_dir + '/' + 'rnn_label.txt'
label_file = open(label_path_dir, 'r')

# In[12]:


label_lines = label_file.readlines()


# In[13]:


#len(label_lines)


# In[14]:


#print(label_lines)


# In[15]:
label_list = []
time_list = []
time = []
step = 0
p = 0
for line in label_lines: #파일 제일 마지막에 엔터 키 필요
    #print(line, end='')
    label_list.append(line.split(" a ")[1].split(" ")[0].replace(",", "")) # person, car ,drone 분류 코드
    if line.count('(') == 0:
        #print('전구간')
        time_list.append(['0',str(len(data_list_seconds[p]))])
    else:
        time_range = line.split("(")[line.count('(')].split(")")[0].split(", ") # 시간 부분만 추출
        for i in range(len(time_range)):
            time.append(time_range[i].split('~'))
        time_list.append(time)
        time = []
    p += 1
    step += 1
    #print("")
    
for step in range(len(label_list)):
    print(step+1,"번째 파일 종류 ", label_list[step])
    print(time_list[step])
'''  
# In[16]:




