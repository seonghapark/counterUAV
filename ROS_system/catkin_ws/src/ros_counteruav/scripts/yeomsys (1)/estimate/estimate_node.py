import numpy as np
import os

index = 0
file_num = 0#0 to 23 0은 rnn_label.txt파일 첫번째 파일을 뜻
result = 0
time_list = np.load('time_list.npy', allow_pickle=True)#[[파일 하나],[[start, finish],..],..]
label_list = np.load('label_list.npy', allow_pickle=True)#[person,person,car,dron,..]
#path_dir = './scripts/raw_data/'
#file_list = os.listdir(path_dir)

print(time_list[file_num])
print(label_list[file_num])

def callback(msg):
      global result
      answer = label_list[file_num]

      who = msg.who
      time = msg.time

      for i in range(0,len(time_list[file_num])):
            start = time_list[file_num][i][0]
            finis = time_list[file_num][i][1]
            if time >= start || time <= finis:
                  if answer == who:
                        print('O')
                        result = result + 1
                  else:
                        print('X')
                  break

def estimate():
      
      print(result/(time_list[file_num][-1][1]))

            

if __name__ == __main__:
      estimate()
