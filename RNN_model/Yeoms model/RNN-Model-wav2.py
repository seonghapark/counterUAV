import glob
import os
import random
import librosa
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.python.ops import rnn, rnn_cell
import numpy as np

plt.style.use('ggplot')

def windows(data, window_size):
    start = 0
    while start < len(data):
        yield start, start + window_size
        start += (window_size / 2)

# 각 33개 input, 각 6개 label
        
def extract_features(file_path, file_label, file_ext="*.wav",bands = 20, frames = 41):
    window_size = 512 * (frames - 1)
    mfccs = []
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
    for (start,end) in windows(sound_clip,window_size):
        start = int(start)
        end = int(end)
        if(len(sound_clip[start:end]) == window_size):
            signal = sound_clip[start:end]
            mfcc = librosa.feature.mfcc(y=signal, sr=s, n_mfcc = bands).T.flatten()[:, np.newaxis].T
            mfccs.append(mfcc)
            labels.append(label_code)         
    features = np.asarray(mfccs).reshape(len(mfccs),frames,bands)
    return np.array(features), np.array(labels,dtype = np.int)

def one_hot_encode(labels):
    n_labels = len(labels)
    n_unique_labels = len(np.unique(labels))
    one_hot_encode = np.zeros((n_labels,n_unique_labels))
    one_hot_encode[np.arange(n_labels), labels] = 1
    return one_hot_encode

wav_file_path_training = 'C://Users/승윤/Desktop/purdue/연구자료/RNN_model/heewon-model/wav_data/train/'
file_list_training = os.listdir(wav_file_path_training)

tr_features = []
tr_labels = []
for f in file_list_training:
    file_label = f.split("_")[0]
    #if file_label=='person' or file_label=='drone': ## 2개씩만 하는 코드
     #   continue
    features_temp, labels_temp = extract_features(wav_file_path_training + f, file_label)
    for tr_f in features_temp:
        tr_features.append(tr_f)
    for tr_l in labels_temp:
        tr_labels.append(tr_l)
    

tmp = [[x,y] for x,y in zip(tr_features, tr_labels)]
random.shuffle(tmp)
tr_features = [n[0] for n in tmp]
tr_labels = [n[1] for n in tmp]


wav_file_path_test = 'C://Users/승윤/Desktop/purdue/연구자료/RNN_model/heewon-model/wav_data/test/'
file_list_test = os.listdir(wav_file_path_test)

ts_features = []
ts_labels = []
for f in file_list_test:
    file_label = f.split("_")[0]
    #if file_label=='' or file_label=='': ## 2개씩만 하는 코드
     #   continue
    features_temp, labels_temp = extract_features(wav_file_path_test + f, file_label)
    for ts_f in features_temp:
        ts_features.append(ts_f)
    for ts_l in labels_temp:
        ts_labels.append(ts_l)
    
tr_labels = one_hot_encode(tr_labels)
ts_labels = one_hot_encode(ts_labels)

tr_features = np.array(tr_features)
tr_labels = np.array(tr_labels)

ts_features = np.array(ts_features)
ts_labels = np.array(ts_labels)

tf.reset_default_graph()

learning_rate = 0.001
training_iters = 300
batch_size = 54 #1188과 216의 최대공약수는 54
display_step = 200

# Network Parameters
n_input = 20
n_steps = 41
n_hidden = 20
n_classes = 4

#앞에거는 hidden *2, 뒤에거는 n_input + n_hidden

x = tf.placeholder("float", [None, n_steps, n_input])
y = tf.placeholder("float", [None, n_classes])

weight = tf.Variable(tf.random_normal([n_hidden, n_classes]))
bias = tf.Variable(tf.random_normal([n_classes]))

def RNN(x, weight, bias):
    #cell = rnn_cell.LSTMCell(n_hidden,state_is_tuple = True)
    cell = rnn_cell.LSTMCell(n_hidden)
    cell = rnn_cell.MultiRNNCell([cell] * 8, state_is_tuple=True)
    output, state = tf.nn.dynamic_rnn(cell, x, dtype = tf.float32)
    print(1, output)
    output = tf.transpose(output, [1, 0, 2])
    print(1, output)
    last = tf.gather(output, int(output.get_shape()[0]) - 1)
    print(output.get_shape())
    print(1, last)
    return tf.nn.softmax(tf.matmul(last, weight) + bias)

prediction = RNN(x, weight, bias)
print(prediction)

# Define loss and optimizer
loss_f = -tf.reduce_sum(y * tf.log(prediction))
optimizer = tf.train.AdamOptimizer(learning_rate = learning_rate).minimize(loss_f)

# Evaluate model
correct_pred = tf.equal(tf.argmax(prediction,1), tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# Initializing the variables
init = tf.global_variables_initializer()

with tf.Session() as session:
    session.run(init)
        
    training_epochs = 15000
    for epoch in range(training_epochs):
        avg_cost = 0
        total_batch = int(len(tr_features) / batch_size)
     
        for i in range(total_batch):
            start = ((i+1) * batch_size) - batch_size
            end = ((i+1) * batch_size)
            batch_x = tr_features[start:end]
            batch_y = tr_labels[start:end]
                    
            _, c = session.run([optimizer, loss_f], feed_dict={x: batch_x, y : batch_y})
            avg_cost += c / total_batch
     
        print('Epoch:', '%04d' % (epoch + 1), 'cost =', '{:.9f}'.format(avg_cost), end='')
        print('Test accuracy: ',round(session.run(accuracy, feed_dict={x: ts_features, y: ts_labels}) , 3))
    print('Learning Finished!')
    saver = tf.train.Saver()
    saver.save(session, './cuav_rnn.ckpt')
    print('Graph Saved! ')
    
'''
    for itr in range(training_iters):    
        offset = (itr * batch_size) % (tr_labels.shape[0] - batch_size)
        batch_x = tr_features[offset:offset + batch_size]
        batch_y = tr_labels[offset:offset + batch_size]
        _, c = session.run([optimizer, loss_f],feed_dict={x: batch_x, y : batch_y})
            
        #if epoch % display_step == 0:
        if itr % 100 == 0:
            # Calculate batch accuracy
            acc = session.run(accuracy, feed_dict={x: batch_x, y: batch_y})
            # Calculate batch loss
            loss = session.run(loss_f, feed_dict={x: batch_x, y: batch_y})
            print("Iter " + str(itr) + ", Minibatch Loss= " + 
                  "{:.6f}".format(loss) + ", Training Accuracy= " + 
                  "{:.5f}".format(acc))
'''







