import tensorflow as tf
import tensorflow.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from feature_extract import FeatureParser
from sklearn.metrics import precision_recall_fscore_support

training_epochs = 2000

class FeedForward():
    def __init__(self, n_dim, n_classes, lr):
        self.opt = {}
        self.opt['n_dim'] = n_dim
        self.opt['n_classes'] = n_classes
        self.opt['learning_rate'] = lr
        self.opt['std'] = 1 / np.sqrt(n_dim)
        self.opt['num_hidden1'] = 500
        self.opt['num_hidden2'] = 1000
        self.opt['num_hidden3'] = 700

    def train_layers(self, train_x, train_y, test_x, test_y):
        params = {}

        X = tf.placeholder(tf.float32, [None, self.opt['n_dim']])
        Y = tf.placeholder(tf.float32, [None, self.opt['n_classes']])
        keep_prob = tf.placeholder(tf.float32) #for dropout

        params['W1'] = tf.Variable(tf.random_normal([self.opt['n_dim'], self.opt['num_hidden1']], mean = 0, stddev=self.opt['std']))
        params['b1'] = tf.Variable(tf.random_normal([self.opt['num_hidden1']], mean = 0, stddev=self.opt['std']))
        params['a1'] = nn.sigmoid(tf.matmul(X, params['W1']) + params['b1'])
        params['dropout1'] = nn.dropout(params['a1'], keep_prob)

        params['W2'] = tf.Variable(tf.random_normal([self.opt['num_hidden1'], self.opt['num_hidden2']], mean = 0, stddev=self.opt['std']))
        params['b2'] = tf.Variable(tf.random_normal([self.opt['num_hidden2']], mean=0, stddev=self.opt['std']))
        params['a2'] = nn.relu(tf.matmul(params['dropout1'], params['W2']) + params['b2'])
        params['dropout2'] = nn.dropout(params['a2'], keep_prob)

        params['W3'] = tf.Variable(tf.random_normal([self.opt['num_hidden2'], self.opt['num_hidden3']], mean = 0, stddev=self.opt['std']))
        params['b3'] = tf.Variable(tf.random_normal([self.opt['num_hidden3']], mean=0, stddev=self.opt['std']))
        params['a3'] = nn.tanh(tf.matmul(params['dropout2'], params['W3']) + params['b3'])
        params['dropout3'] = nn.dropout(params['a3'], keep_prob)

        params['outW'] = tf.Variable(tf.random_normal([self.opt['num_hidden3'], self.opt['n_classes']], mean=0, stddev=self.opt['std']))
        params['outb'] = tf.Variable(tf.random_normal([self.opt['n_classes']], mean=0, stddev=self.opt['std']))

        out = nn.softmax(tf.matmul(params['dropout3'], params['outW']) + params['outb'])

        cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(out), reduction_indices=[1]))
        optimizer = tf.train.AdamOptimizer(self.opt['learning_rate']).minimize(cost)

        correct_pred = tf.equal(tf.argmax(out, 1), tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

        cost_history = np.empty(shape=[1], dtype=float)
        y, y_pred = None, None

        #reshape labels into a one hot vector
        f = FeatureParser()
        train_y = f.one_hot_encode(train_y)
        test_y = f.one_hot_encode(test_y)        

        print('TRAIN_ONE_HOT_LABEL{}'.format(train_y))

        print('Training...')
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            for epoch in range(training_epochs):
                _, loss, acc = sess.run([optimizer, cost, accuracy], feed_dict={X:train_x, Y:train_y, keep_prob: 0.5})
                cost_history = np.append(cost_history, loss)
                if epoch % 50 == 0:
                    print('Epoch#', epoch, 'Cost:', loss, 'Train acc.:', acc)
            
            y_pred = sess.run(tf.argmax(out, 1), feed_dict={X: test_x, keep_prob: 1.0})
            y = sess.run(tf.argmax(test_y, 1))

            print("Test accuracy: ", round(sess.run(accuracy, feed_dict={X: test_x, Y: test_y, keep_prob:1.0}), 3))

        fig = plt.figure(figsize=(10, 8))
        plt.plot(cost_history)
        plt.xlabel('Iterations')
        plt.ylabel('Cost')
        plt.axis([0, training_epochs, 0, np.max(cost_history)])
        plt.show()

        precision, recall, f_score, s = precision_recall_fscore_support(y, y_pred, average='micro')
        print('F score:', round(f_score, 3))

#Convolutional Neural Network for urban sound classification given the UrbanSound8K dataset
class ConvNet():
    def __init__(self, n_dim, n_classes, lr, frames, bands, num_ch, batch_size, k_size, hidden, depth):
        self.opt = {}
        self.opt['n_dim'] = n_dim
        self.opt['n_classes'] = n_classes
        self.opt['learning_rate'] = lr
        self.opt['std'] = 1 / np.sqrt(n_dim)
        self.opt['frames'] = frames
        self.opt['bands'] = bands
        self.opt['num_channels'] = num_ch
        self.opt['batch_size'] = batch_size
        self.opt['k_size'] = k_size
        self.opt['num_hidden'] = hidden
        self.opt['depth'] = depth

    def weight_variable(self, shape):
        initial = tf.truncated_normal(shape, stddev=0.1, dtype=tf.float64)
        return tf.Variable(initial)

    def bias_variable(self, shape):
        initial = tf.constant(1.0, shape = shape)
        return tf.Variable(initial)

    def conv2d(self, x, W):
        return nn.conv2d(x, W, strides=[1,2,2,1], padding='SAME')

    def apply_convolution(self, x, k_size, num_ch, depth):
        weights = self.weight_variable([k_size, k_size, num_ch, depth])
        biases = self.bias_variable([depth])
        return nn.relu(tf.add(self.conv2d(x, weights), biases))

    def apply_max_pool(self, x, k_size, stride_size):
        return nn.max_pool(x, k_size=[1, k_size, k_size, 1], strides=[1, stride_size, stride_size, 1], padding='SAME')

    def train_layers(self, train_x, train_y, test_x, test_y):
        X = tf.placeholder(tf.float32, shape=[None, self.opt['bands'], self.opt['frames'], self.opt['num_channels']])
        Y = tf.placeholder(tf.float32, shape=[None, self.opt['n_classes']])

        conv_layer = self.apply_convolution(train_x, self.opt['k_size'], self.opt['num_channels'], self.opt['depth'])

        shape = conv_layer.get_shape().as_list()
        conv_flat = tf.reshape(conv_layer, [-1, shape[1] * shape[2], shape[3]])

        f_weights = self.weight_variable(shape[1] * shape[2] * self.opt['depth'], self.opt['num_hidden'])
        f_biases = self.bias_variable([self.opt['num_hidden']])
        f = nn.sigmoid(tf.add(tf.matmul(conv_flat, f_weights), f_biases))

        out_weights = self.weight_variable([self.opt['num_hidden'], self.opt['n_classes']])
        out_biases = bias_variable([self.opt['n_classes']])
        out = nn.softmax(tf.matmul(f, out_weights) + out_biases)

        cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(out), reduction_indices=[1]))
        #cross_entropy = -tf.reduce_sum(Y * tf.log(out))
        optimizer = tf.train.AdamOptimizer(learning_rate=self.opt['learning_rate']).minimize(cost)
        correct_pred = tf.equal(tf.argmax(out, 1), tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

        cost_history = np.empty(shape=[1], dtype=float)
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            for i in range(training_epochs):
                offset = (i * self.opt['batch_size']) % (train_y.shape[0] - batch_size)
                batch_x = train_x[offset:(offset + batch_size), :, :, :]
                batch_y = train_y[offset:(offset + batch_size), :]

                _, loss = sess.run([optimizer, cost], feed_dict={X: batch_x, Y: batch_y})
                cost_history = np.append(cost_history, loss)

            print('Test accuracy: ', round(sess.run(accuracy, feed_dict={X: test_x, Y: test_y}), 3))
            fig = plt.figure(figsize=(15,10))
            plt.plot(cost_history)
            plt.axis([0, training_epochs, o, np.max(cost_history)])
            plt.show()
