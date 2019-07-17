import tensorflow as tf
import numpy as np

train_time = 60
train_data = []
tmp_data = []
read_data = np.load('data_list_sec.npy', allow_pickle=True)
#person
for i in range(38,68,1):#13
    tmp_data.append(read_data[1][i])
train_data.append(tmp_data)
tmp_data = []
#car
for i in range(0,16,1):
    tmp_data.append(read_data[21][i])
for i in range(40,54,1):
    tmp_data.append(read_data[21][i])
train_data.append(tmp_data)
tmp_data = []
#dron
for i in range(1,9,1):#8
    tmp_data.append(read_data[11][i])
for i in range(36,47,1):#11
    tmp_data.append(read_data[11][i])
for i in range(46,49,1):#3
    tmp_data.append(read_data[11][i])
for i in range(62,70,1):
    tmp_data.append(read_data[11][i])
train_data.append(tmp_data)
tmp_data = []
#other
for i in range(37,67,1):
    tmp_data.append(read_data[0][i])
train_data.append(tmp_data)
train_data = np.array(train_data)
tmp_data = []
#train_data = (4,30,2931)
#(0,0~29,0~2930) = 사람
#(1,0~29,0~2930)=차
#(2,0~29,0~2930)=드론
#(3,0~29,0~2930)=기타
#RNN
train_data = np.array(train_data)

batch_size = 4
input_dim = 2931
sequence = 30
hidden = 5
out_dim = 1
class_num = out_dim

x_d = train_data
y_d = [[0],[1],[2],[3]]
y_d = np.array(y_d)
print(x_d.shape, y_d.shape)

x=tf.placeholder(tf.float32,shape=[None, sequence, input_dim])
y=tf.placeholder(tf.float32,shape=[None, out_dim])
#y_one = tf.one_hot(y,class_num)

cell = tf.contrib.rnn.BasicLSTMCell(num_units=hidden,state_is_tuple=True, activation=tf.tanh)
output, _stat = tf.nn.dynamic_rnn(cell, x, dtype=tf.float32)
y_pred = tf.contrib.layers.fully_connected(output[:,-1], out_dim, activation_fn=None)

#y_pred (?,30,1) y (?,4) output (?,30,1)
#w=tf.ones([batch_size, sequence])
#seq_loss=tf.contrib.seq2seq.sequence_loss(logits=output, targets=y, weights=w)
#loss=tf.reduce_mean(seq_loss)

loss = tf.reduce_sum(tf.square(y_pred - y))

opt = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

se=tf.Session()
se.run(tf.global_variables_initializer())

for steps in range(2000):
    _, lo= se.run([opt,loss],feed_dict={x:x_d, y:y_d})
    pre_y = se.run(y_pred,feed_dict={x:x_d})
    if steps%20==0:
        print(steps,' 번째 loss: ',lo, '\n예측\n',pre_y, '답\n',y_d)

#pre_y = se.run(y_pred,feed_dict={x:x_d})
#print('예측: ',pre_y, '실제: ',y)
