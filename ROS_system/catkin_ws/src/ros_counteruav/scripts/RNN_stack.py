#!/usr/bin/env python3
import rospy
import numpy as np
from scipy.io import wavfile
import librosa
from ros_counteruav.msg import fakedata
from ros_counteruav.msg import wav

sec = 0
time = 1
sec5 = []

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

time = 0#global error
def callback(msg):
    global sec
    global time
    global sec5

    datalist = []
    synclist = []
    sync, data = parse(msg.data)
    datalist.append(data)
    synclist.append(sync)
    audio = np.vstack((sync,data))
    wavfile.write("parse.wav", 5862, audio.T.astype(np.int16))
    Y, _ = librosa.load("parse.wav", sr=5862, mono=False)
    print(len(Y[1]))
    print(Y[1].shape)
    pub = rospy.Publisher('wav_list', wav, queue_size=1)
    message = wav()
    print(Y[1].astype(float))
    mess = Y[1].astype(float)
    mess = mess.tolist()
    print(len(mess))
    if sec == 5:
        print('send', time)
        message.wavdata = sec5
        message.time = time
        pub.publish(message)
        sec = sec - 1
        sec5 = sec5[len(mess)+1:]
    else:
        print('not send', time)
        sec = sec + 1
        sec5.extend(mess)

    print(len(sec5))
    time = time + 1
    print(time)

def RNN_stack():
    rospy.init_node('RNN_stack', anonymous=True)
    rospy.Subscriber('chatter', fakedata, callback)
    print('RNN_stack ready')
    rospy.spin()

if __name__ == "__main__":
    RNN_stack()