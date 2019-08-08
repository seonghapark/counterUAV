#!/usr/bin/env python3
import glob
import matplotlib.pyplot as plt
import rospy
import tensorflow as tf
import numpy as np
#from scipy.fftpack import fft
import librosa
import random
import os
from scipy.io import wavfile
from ros_counteruav.msg import testdata
from ros_counteruav.msg import objectinfo
from tensorflow.python.ops import rnn, rnn_cell

class RadarBinaryParser():
    def __init__(self, raw_data, sr=5862):
        self.raw_data = raw_data
        self.sr = sr
        self.sync = None
        self.data = None

    '''get sync, data and headers from text binary file.
    '''

    def parse(self):
        data = bytearray(self.raw_data)
        # print(len(data))
        # parse the sync and data signal in bytearray
        if len(data) < 2:
            return None, None
        if (data[0] >> 6) > 0: # '11'로 시작하는 데이터 일 때, 맨 앞의 데이터 삭제
            del data[:1]
        if len(data) % 2 == 1: # 전체 데이터 개수가 홀수인 경우
            del data[-1:]

        values = []
        sync = []
        for index in range(0, len(data), 2):
            if (data[index] >> 6) > 0 and index+2 <len(data): #내가 추가한 코드
                index_2 = index + 1
            else:
                index_2 = index
            high = data[index_2] & 0x1F
            low = data[index_2 + 1] & 0x1F
            values.append(high << 5 | low) 
            sync.append(True if (data[index_2] >> 5) == 1 else False)

        sync = sync #sync = np.array(sync)
        data = values #data = np.array(values)
            
        # print(self.sync, self.data, len(self.sync), len(self.data))
        return sync, data
        
###############################################################################

class CUAV_Model:
    
    def __init__(self):
        self.n_hidden = 40
        pass

    def windows(self, data, window_size):
        start = 0
        while start < len(data):
            yield start, start + window_size
            start += (window_size / 2)

    def extract_features(self, file_path, file_label, file_ext="*.wav",bands = 20, frames = 41):
        window_size = 512 * (frames - 1)
        mfccs = []
        log_specgrams = []
        features = []
        labels = []
        sound_clip, s = librosa.load(file_path)
        #print(type(sound_clip))
        if file_label=='other':
            label_code = 0
        elif file_label=='person':
            label_code = 1
        elif file_label=='car':
            label_code = 2
        elif file_label=='drone':
            label_code = 3

        #print(file_label, label_code)
        for (start,end) in self.windows(sound_clip,window_size):
            start = int(start)
            end = int(end)
            if(len(sound_clip[start:end]) == window_size):
                signal = sound_clip[start:end]

                melspec = librosa.feature.melspectrogram(signal, n_mels = bands)
                logspec = librosa.amplitude_to_db(melspec)
                logspec = logspec.T.flatten()[:, np.newaxis].T
                #print(1, logspec.shape)
                log_specgrams.append(logspec)

                mfcc = librosa.feature.mfcc(y=signal, sr=s, n_mfcc = bands).T.flatten()[:, np.newaxis].T
                mfccs.append(mfcc)
                #print(2, mfcc.shape)
                features = np.hstack((mfccs, log_specgrams))
                labels.append(label_code)         
        features = np.asarray(features).reshape(len(mfccs), frames, bands*2)
        #print(features.shape)
        return np.array(features), np.array(labels,dtype = np.int)

    def extract_features_for_predict(self, file_path, bands = 20, frames = 41):
        window_size = 512 * (frames - 1)
        mfccs = []
        log_specgrams = []
        features = []
        sound_clip, s = librosa.load(file_path)

        for (start,end) in self.windows(sound_clip,window_size):
            start = int(start)
            end = int(end)
            if(len(sound_clip[start:end]) == window_size):
                signal = sound_clip[start:end]

                melspec = librosa.feature.melspectrogram(signal, n_mels = bands)
                logspec = librosa.amplitude_to_db(melspec)
                logspec = logspec.T.flatten()[:, np.newaxis].T
                log_specgrams.append(logspec)

                mfcc = librosa.feature.mfcc(y=signal, sr=s, n_mfcc = bands).T.flatten()[:, np.newaxis].T
                mfccs.append(mfcc)
                features = np.hstack((mfccs, log_specgrams))      

        features = np.asarray(features).reshape(len(mfccs), frames, bands*2)
        #print(features.shape)
        return np.array(features)

    def one_hot_encode(self, labels):
        n_labels = len(labels)
        n_unique_labels = len(np.unique(labels))
        one_hot_encode = np.zeros((n_labels,n_unique_labels))
        one_hot_encode[np.arange(n_labels), labels] = 1
        return one_hot_encode
    
    def make_data(self):
        wav_file_path_training = '/home/project/counterUAV/ROS_system/catkin_ws/src/ros_counteruav/scripts/wav_data/train/'
        file_list_training = os.listdir(wav_file_path_training)

        tr_features = []
        tr_labels = []
        for f in file_list_training:
            file_label = f.split("_")[0]
            #if file_label=='person' or file_label=='car':
             #   continue
            features_temp, labels_temp = self.extract_features(wav_file_path_training + f, file_label)
            for tr_f in features_temp:
                tr_features.append(tr_f)
            for tr_l in labels_temp:
                tr_labels.append(tr_l)


        tmp = [[x,y] for x,y in zip(tr_features, tr_labels)]
        random.shuffle(tmp)
        tr_features = [n[0] for n in tmp]
        tr_labels = [n[1] for n in tmp]

        wav_file_path_test = '/home/project/counterUAV/ROS_system/catkin_ws/src/ros_counteruav/scripts/wav_data/test/'
        file_list_test = os.listdir(wav_file_path_test)

        ts_features = []
        ts_labels = []
        for f in file_list_test:
            file_label = f.split("_")[0]
            #if file_label=='person' or file_label=='car':
             #   continue
            features_temp, labels_temp = self.extract_features(wav_file_path_test + f, file_label)
            for ts_f in features_temp:
                ts_features.append(ts_f)
            for ts_l in labels_temp:
                ts_labels.append(ts_l)

        tr_labels = self.one_hot_encode(tr_labels)
        ts_labels = self.one_hot_encode(ts_labels)

        self.tr_features = np.array(tr_features)
        self.tr_labels = np.array(tr_labels)

        self.ts_features = np.array(ts_features)
        self.ts_labels = np.array(ts_labels)
        
        
    def RNN(self, x, weight, bias):
        cell = rnn_cell.LSTMCell(self.n_hidden,state_is_tuple = True)
        cell = rnn_cell.MultiRNNCell([cell] * 8, state_is_tuple=True)
        output, state = tf.nn.dynamic_rnn(cell, x, dtype = tf.float32)
        output = tf.transpose(output, [1, 0, 2])
        last = tf.gather(output, int(output.get_shape()[0]) - 1)
        return tf.nn.softmax(tf.matmul(last, weight) + bias)
    
    def graph_setting(self):
        tf.reset_default_graph()
        self.session = tf.Session()

        learning_rate = 0.0003

        # Network Parameters
        n_input = 40
        n_steps = 41
        n_classes = 4

        # hidden *2=n_input + n_hidden

        self.x = tf.placeholder("float", [None, n_steps, n_input])
        self.y = tf.placeholder("float", [None, n_classes])

        weight = tf.Variable(tf.random_normal([self.n_hidden, n_classes]))
        bias = tf.Variable(tf.random_normal([n_classes]))
        
        self.prediction = self.RNN(self.x, weight, bias)
        self.prediction_str = tf.argmax(self.prediction, 1)
        #prediction_str, prediction, x, 
        # Define loss and optimizer
        self.loss_f = -tf.reduce_sum(self.y * tf.log(self.prediction))
        self.optimizer = tf.train.AdamOptimizer(learning_rate = learning_rate).minimize(self.loss_f)

        # Evaluate model
        self.correct_pred = tf.equal(tf.argmax(self.prediction,1), tf.argmax(self.y,1))
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_pred, tf.float32))

        # Initializing the variables
        
    def training(self):
        init = tf.global_variables_initializer()
        self.session.run(init)

        training_epochs = 10000
        batch_size = 54 #1188 216 54
        
        for epoch in range(training_epochs):
            avg_cost = 0
            total_batch = int(len(self.tr_features) / batch_size)

            for i in range(total_batch):
                start = ((i+1) * batch_size) - batch_size
                end = ((i+1) * batch_size)
                batch_x = self.tr_features[start:end]
                batch_y = self.tr_labels[start:end]

                _, c = self.session.run([self.optimizer, self.loss_f], feed_dict={self.x: batch_x, self.y : batch_y})
                avg_cost += c / total_batch

            print('Epoch:', '%04d' % (epoch + 1), 'cost =', '{:.9f}'.format(avg_cost), end='')
            print('Test accuracy: ',round(self.session.run(self.accuracy, feed_dict={self.x: self.ts_features, self.y: self.ts_labels}) , 3))
            if epoch % 100 == 0:
                self.save_network(epoch)
        
        print('Learning Finished!')

        
    def save_network(self, step):
        saver = tf.train.Saver()
        saver.save(self.session, './rnn_graph_save/cuav_rnn.ckpt', step)
        print('Graph Saved! ')
        
    def predict(self, file_source):
        #print(file_source)
        data_to_predict = self.extract_features_for_predict(file_source)
        #print(data_to_predict.shape)
        result_list = self.session.run(self.prediction_str, feed_dict={self.x: data_to_predict})
        #print(result_list)
        result_list = list(result_list)
        label_count = {'others': 0, 'person': 0, 'car': 0, 'drone': 0,}

        total = 0
        for i, key in enumerate(list(label_count.keys())):
            label_count[key] = (result_list.count(i))
            print(key, int(label_count[key])/data_to_predict.shape[0])

        t = list(zip(list(label_count.values()), list(label_count.keys())))
        t.sort(reverse=True)
        return t

        #for i in range(data_to_predict.shape[0]):
            #temp_output = session.run(prediction, feed_dict={x: data_to_predict[i]})
            #print(temp_output)
        
    def restore_graph(self, step):
        save_file = './rnn_graph_save/cuav_rnn.ckpt' + '-' + str(step)
        saver = tf.train.Saver()
        saver.restore(self.session, save_file)


###############################################################################
def RNN():
    global model
    who = model.predict("./radar.wav")
    print(who)
    RAWS_send = rospy.Publisher('RAWS_send', objectinfo, queue_size=1)
    message = objectinfo()
    message.who = str(who[0][1], 'utf-8')
    RAWS_send.publish(who)


def callback(msg):
    #print('{}'.format(msg.some_int))
    #print(len(msg.some_int))
    wav = RadarBinaryParser(msg.some_int, sr=5862)
    sync, data = wav.parse()
    #audio = np.vstack((sync, data))
    audio = np.vstack((sync,data))
    #sec_time += 1
    #wavfile.write(str(random.randint(1,500)) + ".wav", wav.sr, audio.T.astype(np.int16))#make wav file
    wavfile.write("radar.wav", wav.sr, audio.T.astype(np.int16))#make wav file
    print('new wav file')
    RNN()

def RAWS():
    rospy.init_node('RAWS', anonymous=True)
    print('RAWS ready')
    rospy.Subscriber('MCRC_send', testdata, callback)
    rospy.spin()

if __name__ == '__main__':
    model = CUAV_Model()
    model.graph_setting()
    model.restore_graph(1100)
    print('RNN Model is ready')
    RAWS()
