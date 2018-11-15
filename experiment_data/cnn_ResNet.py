import tensorflow as tf
import os
from os.path import isfile
import numpy as np
import log_spec as ls
import time
import matplotlib.pyplot as plt

start_time = time.time()

FILE_EXT='*.wav'

frames = 41 
bands = 60

feature_size = 2460 
num_channels = 2
num_labels = 4

batch_size = 16 
kernel_size = 3 #filter size
num_hidden = 200 #fully connected node 개수
depth = 20 #filter 개수

PARENT_DIR='../experiment_data'
learning_rate = 1e-6
total_epoch = 2000 #training set 전체를 한번 돌림

tr_sub_dirs= ['fold1','fold2']
tr_features, tr_labels = ls.extract_log_spec(PARENT_DIR, tr_sub_dirs, file_ext=FILE_EXT, bands=60, frames=41)
tr_labels = ls.one_hot_encode(tr_labels)

ts_sub_dirs= ['fold3']
ts_features, ts_labels = ls.extract_log_spec(PARENT_DIR,ts_sub_dirs, file_ext=FILE_EXT, bands=60, frames=41)
ts_labels = ls.one_hot_encode(ts_labels)

def weight_variable(shape): #filter 만들기
    initial = tf.truncated_normal(shape, stddev = 0.1)
    return tf.Variable(initial)

def bias_variable(shape): #bias 만들기
    initial = tf.constant(1.0, shape = shape)
    return tf.Variable(initial)

def conv2d(x, W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1], padding='SAME')

def apply_convolution(x,kernel_size,num_channels,depth):
    weights = weight_variable([kernel_size, kernel_size, num_channels, depth])
    biases = bias_variable([depth])
    return tf.nn.relu(tf.add(conv2d(x, weights),biases)) #convol한 결과에 bias 더해.

def apply_max_pool(x,kernel_size,stride_size):
    return tf.nn.max_pool(x, ksize=[1, kernel_size, kernel_size, 1], 
                          strides=[1, stride_size, stride_size, 1], padding='SAME')

def linear_proj(x):
    # Linearly projecting input X via a linear mapping function H(X)
    weights = weight_variable([1, 1, 2, 20])
    shortcut = tf.nn.conv2d(x, weights, strides=[1,1,1,1], padding='SAME')
    return shortcut

X = tf.placeholder(tf.float32, shape=[None,bands,frames,num_channels])
Y = tf.placeholder(tf.float32, shape=[None,num_labels])

shape = X.get_shape().as_list()
print(shape)

cov1 = apply_convolution(X,kernel_size,num_channels,depth) #initialize weight variable(filters)
shape = cov1.get_shape().as_list()
print(shape)
pool1 = apply_max_pool(cov1, kernel_size, 1)
shape = pool1.get_shape().as_list()
print(shape)

cov2 = apply_convolution(pool1,kernel_size,20,depth) #initialize weight variable(filters)
shape = cov2.get_shape().as_list()
print(shape)
pool2 = apply_max_pool(cov2, kernel_size, 1)
shape = pool2.get_shape().as_list()
print(shape)

shortcut = linear_proj(X)
conv_out = tf.add(pool2, shortcut)
print('conv_out before flattening:', conv_out.get_shape())
shape = conv_out.get_shape().as_list()

conv_flat = tf.reshape(conv_out, [-1, shape[1] * shape[2] * shape[3]]) #fully_connected에 넣기 위해.

f_weights = weight_variable([shape[1] * shape[2] * depth, num_hidden]) #fully_connected weight
f_biases = bias_variable([num_hidden]) #fully_connected bias
f = tf.nn.sigmoid(tf.add(tf.matmul(conv_flat, f_weights),f_biases))

out_weights = weight_variable([num_hidden, num_labels]) #full_output 사이의 weight
out_biases = bias_variable([num_labels])
y_ = tf.nn.softmax(tf.matmul(f, out_weights) + out_biases)

loss = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(y_), reduction_indices=[1]))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)
correct_prediction = tf.equal(tf.argmax(y_,1), tf.argmax(Y,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

cost_history = np.empty(shape=[1],dtype=float)
with tf.Session() as session:
    tf.global_variables_initializer().run()

    for i in range(total_epoch):    
        offset = (i * batch_size) % (tr_labels.shape[0] - batch_size)
        batch_x = tr_features[offset:(offset + batch_size), :, :, :]
        batch_y = tr_labels[offset:(offset + batch_size), :]
        
        _, c = session.run([optimizer, loss],feed_dict={X: batch_x, Y : batch_y})
        cost_history = np.append(cost_history,c)
    
    print('Test accuracy: ',round(session.run(accuracy, feed_dict={X: ts_features, Y: ts_labels}) , 3))
    fig = plt.figure(figsize=(15,10))
    plt.plot(cost_history)
    plt.axis([0,total_epoch,0,np.max(cost_history)])
    plt.show()

print("--- %s seconds ---" % (time.time() - start_time))
