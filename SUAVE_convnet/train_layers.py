import tensorflow as tf
import numpy as np
from collections import OrderedDict
import matplotlib.pyplot as plt
from feature_extract import FeatureParser
from sklearn.metrics import precision_recall_fscore_support

BATCH_NORM_EPSILON = 1e-5
BATCH_NORM_DECAY = 0.9

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
        params['a1'] = tf.nn.sigmoid(tf.matmul(X, params['W1']) + params['b1'])
        params['dropout1'] = tf.nn.dropout(params['a1'], keep_prob)

        params['W2'] = tf.Variable(tf.random_normal([self.opt['num_hidden1'], self.opt['num_hidden2']], mean = 0, stddev=self.opt['std']))
        params['b2'] = tf.Variable(tf.random_normal([self.opt['num_hidden2']], mean=0, stddev=self.opt['std']))
        params['a2'] = tf.nn.relu(tf.matmul(params['dropout1'], params['W2']) + params['b2'])
        params['dropout2'] = tf.nn.dropout(params['a2'], keep_prob)

        params['W3'] = tf.Variable(tf.random_normal([self.opt['num_hidden2'], self.opt['num_hidden3']], mean = 0, stddev=self.opt['std']))
        params['b3'] = tf.Variable(tf.random_normal([self.opt['num_hidden3']], mean=0, stddev=self.opt['std']))
        params['a3'] = tf.nn.tanh(tf.matmul(params['dropout2'], params['W3']) + params['b3'])
        params['dropout3'] = tf.nn.dropout(params['a3'], keep_prob)

        params['outW'] = tf.Variable(tf.random_normal([self.opt['num_hidden3'], self.opt['n_classes']], mean=0, stddev=self.opt['std']))
        params['outb'] = tf.Variable(tf.random_normal([self.opt['n_classes']], mean=0, stddev=self.opt['std']))

        out = tf.nn.softmax(tf.matmul(params['dropout3'], params['outW']) + params['outb'])

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
    def __init__(self, n_dim, n_classes, lr, frames, bands, num_ch, batch_size, k_size, hidden, depth, epoch):
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
        self.opt['epoch'] = epoch

        self.figure = None

    def weight_variable(self, shape):
        initial = tf.truncated_normal(shape, stddev=0.1, dtype=tf.float32)
        return tf.Variable(initial)

    def bias_variable(self, shape):
        initial = tf.constant(1.0, shape = shape)
        return tf.Variable(initial)

    def conv2d(self, x, W):
        return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding='SAME')

    def apply_convolution(self, x, k_size, num_ch, depth):
        weights = self.weight_variable([k_size, k_size, num_ch, depth])
        biases = self.bias_variable([depth])
        return tf.nn.relu(tf.add(self.conv2d(x, weights), biases))

    def apply_max_pool(self, x, k_size, stride_size):
        return tf.nn.max_pool(x, [1, k_size, k_size, 1], [1, stride_size, stride_size, 1], padding='SAME')

    def batch_norm(self, x, training):
        # Perform batch normalization on parameters
        b_norm = tf.layers.batch_normalization(inputs=x, axis=1, momentum=BATCH_NORM_DECAY, epsilon=BATCH_NORM_EPSILON, center=True, scale=True, training=training, fused=False)

        return b_norm

    def linear_proj(self, x):
        # Linearly projecting input X via a linear mapping function H(X)
        weights = self.weight_variable([1, 1, 2, 30])
        shortcut = tf.nn.conv2d(x, weights, strides=[1,1,1,1], padding='SAME')
        return shortcut

    def train_layers(self, train_x, train_y, test_x, test_y, nlayers, resFlag=False):
        X = tf.placeholder(tf.float32, shape=[None, self.opt['bands'], self.opt['frames'], self.opt['num_channels']])
        Y = tf.placeholder(tf.float32, shape=[None, self.opt['n_classes']])
        keep_prob = tf.placeholder(tf.float32) # 'p' for dropout probability
        #TODO:k_list, ch_list and s_list length and value should be dynamically adjusted
        k_list = [self.opt['k_size'], 3, 3]
        ch_list = [self.opt['num_channels'], 20, 30]
        s_list = [1, 1, 1]

        layers = OrderedDict()
        # 1st conv + batch_norm + pool_layer
        layers['conv1'] = self.apply_convolution(X, k_list[0], ch_list[0], ch_list[1])
        layers['pool1'] = self.apply_max_pool(layers['conv1'], 3, 1)
        layers['norm1'] = self.batch_norm(layers['pool1'], True)

        if nlayers >= 2:
            for idx in range(2, nlayers+1):
                layers['conv' + str(idx)] = self.apply_convolution(layers['norm' + str(idx-1)], k_list[idx-1], ch_list[idx-1], ch_list[idx])
                layers['pool' + str(idx)] = self.apply_max_pool(layers['conv' + str(idx)], k_list[idx-1], s_list[idx - 1])
                layers['norm' + str(idx)] = self.batch_norm(layers['pool' + str(idx)], True)
        print('Layer dict:', layers.keys())
        if resFlag:
            # Skip connection from input(X) to pool_layer2
            shortcut = self.linear_proj(X)
            layers['conv_out'] = tf.add(layers[list(layers.keys())[-1]], shortcut)
        else:
            layers['conv_out'] = layers[list(layers.keys())[-1]]

        layers['conv_out'] = tf.nn.relu(layers['conv_out']) # A ReLU activation coming after element-wise addition
        print('conv_out before flattening:', layers['conv_out'].get_shape())

        shape = layers['conv_out'].get_shape().as_list()
        print('Shape of the last layer\'s output:', shape)
        conv_flat = tf.reshape(layers['conv_out'], [-1, shape[1] * shape[2] * shape[3]]) 

        # print('1, 2 : ', shape[1] , shape[2] , self.opt['depth'], self.opt['num_hidden'])
        f_weights = self.weight_variable([shape[1] * shape[2] * 30, self.opt['num_hidden']])
        f_biases = self.bias_variable([self.opt['num_hidden']])
        print('conv_flat, f_weights : ', conv_flat.shape, f_weights.shape)
        f = tf.nn.sigmoid(tf.add(tf.matmul(conv_flat, f_weights), f_biases))

        out_weights = self.weight_variable([self.opt['num_hidden'], self.opt['n_classes']])
        out_biases = self.bias_variable([self.opt['n_classes']])
        drop_layer = tf.nn.dropout(tf.matmul(f, out_weights) + out_biases, keep_prob)
        out = tf.nn.softmax(drop_layer)

        cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(out), reduction_indices=[1]))
        optimizer = tf.train.AdamOptimizer(learning_rate=self.opt['learning_rate']).minimize(cost)
        correct_pred = tf.equal(tf.argmax(out, 1), tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

        pred_per_classes = tf.nn.in_top_k(out, tf.argmax(Y, 1), 1)

        cost_history = np.empty(shape=[1], dtype=float)
        print('Training...')
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            for i in range(self.opt['epoch']):
                offset = (i * self.opt['batch_size']) % (train_y.shape[0] - self.opt['batch_size'])
                batch_x = train_x[offset:(offset + self.opt['batch_size']), :, :, :]
                batch_y = train_y[offset:(offset + self.opt['batch_size']), :]
                _, loss, acc = sess.run([optimizer, cost, accuracy], feed_dict={X: batch_x, Y: batch_y, keep_prob: 1.0}) #Dropout p=0.5 without batch_norm in action
                cost_history = np.append(cost_history, loss)

                if (i + 1) % 100 == 0:
                    print('Epoch: {}, Cost: {:.3f}, Accuracy: {:.3f}'.format(i + 1, loss, acc))

            # Calculate test batch accuracy
            sum_acc = .0
            count_total = np.array([.0] * self.opt['n_classes'])
            count_answer = np.array([.0] * self.opt['n_classes'])
            total = 0
            for i in range(0, test_x.shape[0], self.opt['batch_size']):

                offset = (int(i/self.opt['batch_size']) * 1) % (test_x.shape[0] - self.opt['batch_size'])
                batch_x = test_x[offset:(offset + self.opt['batch_size']), :, :, :]
                batch_y = test_y[offset:(offset + self.opt['batch_size']), :]

                acc, pred = sess.run([accuracy, pred_per_classes], feed_dict={X: batch_x, Y: batch_y, keep_prob: 1.0})
                sum_acc += acc
                
                correct_label = np.array([-1] * self.opt['batch_size'])

                for i in range(self.opt['batch_size']):
                    correct_label[i] = np.argmax(batch_y, 1)[i] if pred[i] == True else -1
                
                print('pred: ', pred, 'label: ', np.argmax(batch_y, 1))
                # print('pred: ', pred, 'label: ', np.argmax(batch_y, 1), 'correct: ', correct_label)
                # print('correct_label: ', correct_label)
                
                for e in np.argmax(batch_y, 1):
                    count_total[e] += 1

                for e in correct_label:
                    if e != -1:
                        count_answer[e] += 1
                total += 1

            print('Test accuracy: ', round(float(sum_acc / total), 3))
            print('# of answer: ', count_answer, '# of label: ', count_total)
            print('Other accuracy: ', count_answer / count_total)
            
            fig = plt.figure(figsize=(15,10))
            self.figure = fig

            plt.plot(cost_history)
            plt.axis([0, self.opt['epoch'], 0, np.max(cost_history)])
            plt.show()

            sess.close()


class RecurrentNet():
    # Define RNN model
    def __init__(self, n_input, n_steps, n_classes, learning_rate, batch_size, n_hidden, training_epochs):
        self.opt = {}
        self.opt['n_input'] = n_input
        self.opt['n_steps'] = n_steps
        self.opt['n_classes'] = n_classes
        self.opt['learning_rate'] = learning_rate
        self.opt['batch_size'] = batch_size
        self.opt['n_hidden'] = n_hidden
        self.opt['training_epochs'] = training_epochs
        
    def train_layers(self, train_x, train_y, test_x, test_y):
        # setting for hyper-parameter
        tf.reset_default_graph()

        learning_rate = self.opt['learning_rate']
        training_epochs = self.opt['training_epochs']
        batch_size = self.opt['batch_size']
        display_step = 100

        # Network Parameters
        n_input = self.opt['n_input']
        n_steps = self.opt['n_steps']
        n_hidden = self.opt['n_hidden']
        n_classes = self.opt['n_classes']

        X = tf.placeholder("float", [None, n_steps, n_input])
        Y = tf.placeholder("float", [None, n_classes])

        weight = tf.Variable(tf.random_normal([n_hidden, n_classes]))
        bias = tf.Variable(tf.random_normal([n_classes]))

        cell = []
        for i in range(2):
            temp = tf.nn.rnn_cell.LSTMCell(n_hidden, state_is_tuple=True)
            temp = tf.nn.rnn_cell.DropoutWrapper(temp, output_keep_prob=0.5)
            cell.append(temp)

        cell = tf.nn.rnn_cell.MultiRNNCell(cell)
        output, state = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
        output = tf.transpose(output, [1, 0, 2])
        last = tf.gather(output, int(output.get_shape()[0]) - 1)
        prediction = tf.nn.softmax(tf.matmul(last, weight) + bias)

        # Define loss and optimizer
        loss_f = -tf.reduce_sum(Y * tf.log(prediction))
        optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss_f)

        # Evaluate model
        correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
        cost_history = np.array([])

        # Run a tensorflow session
        with tf.Session() as session:
        # Initializing the variables
            session.run(tf.global_variables_initializer())

            for itr in range(training_epochs):
                offset = (itr * batch_size) % (train_y.shape[0] - batch_size)
                batch_x = train_x[offset:(offset + batch_size), :, :]
                batch_y = train_y[offset:(offset + batch_size), :]
                _, c = session.run(
                    [optimizer, loss_f], feed_dict={ X: batch_x, Y: batch_y })
                cost_history = np.append(cost_history, c)

                if itr % display_step == 0:
                    # Calculate batch loss, accuracy
                    loss, acc = session.run(
                        [loss_f, accuracy], feed_dict={ X: batch_x, Y: batch_y })

                    print("Iter " + str(itr) + ", Minibatch Loss= " +
                        "{:.6f}".format(loss) + ", Training Accuracy= " +
                        "{:.5f}".format(acc))

            print('Test accuracy: ', round(session.run(
                accuracy, feed_dict={ X: test_x, Y: test_y }), 3))

            fig = plt.figure(figsize=(15,10))
            plt.plot(cost_history)
            plt.axis([0, training_epochs, 0, np.max(cost_history)])
            plt.show()
