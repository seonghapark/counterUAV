import tensorflow as tf
import tensorflow.contrib as contrib


class RadarNet():
#A convolutional neural network architecture for classifying radar data

    def __init__(self, opt):
        self.batch_size = opt['batch_size']
        self.num_class = opt['num_class']
        self.lr = opt['learning_rate']
        self.dropout = opt['dropout_p']
        self.num_epoch = opt['epoch']

    def model(x):
        #Initialze kernels
        conv1_filter = tf.Variable(tf.truncated_normal(shape=[3, 3, 3, 64], mean=0, stddev=0.08))
        conv2_filter = tf.Variable(tf.truncated_normal(shape=[3, 3, 64, 128], mean=0, stddev=0.08))
        conv3_filter = tf.Variable(tf.truncated_normal(shape=[5, 5, 128, 256], mean=0, stddev=0.08))
        conv4_filter = tf.Variable(tf.truncated_normal(shape=[5, 5, 256, 512], mean=0, stddev=0.08))

        #conv1 -> conv2
        conv1 = tf.nn.conv2d(x, conv1_filter, strides=[1, 1, 1, 1], padding='SAME') #if padding=VALID, then no padding
        conv1 = tf.nn.relu(conv1)
        conv1_pool = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        #batch norm
        conv1_out = tf.layers.batch_normalization(conv1_pool)
        
        #conv2 -> conv3
        conv2 = tf.nn.conv2d(conv1_out, conv2_filter, strides=[1, 1, 1, 1], padding='SAME')
        conv2 = tf.nn.relu(conv2)
        conv2_pool = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        conv2_out = tf.layers.batch_normalization(conv2_pool)
        
        #conv3 -> conv4
        conv3 = tf.nn.conv2d(conv2_out, conv3_filter, strides=[1, 1, 1, 1], padding='SAME')
        conv3 = tf.nn.relu(conv3)
        conv3_pool = tf.nn.max_pool(conv3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        conv3_out = tf.layers.batch_normalization(conv3_pool)
        
        #conv4 -> ffn
        conv4 = tf.nn.conv2d(conv3_out, conv4_filter, strides=[1, 1, 1, 1], padding='SAME') 
        conv4 = tf.nn.relu(conv4)
        conv4_pool = tf.nn.max_pool(conv4, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        conv4_out = tf.layers.batch_normalization(conv4_pool)

        #flatten the pooling layer output 
        conv4_out = contrib.layers.flatten(conv4_out)

        # ffn1
        ffn1 = contrib.layers.fully_connected(inputs=conv4_out, num_outputs=64, activation_fn=tf.nn.relu)
        ffn1 = tf.nn.dropout(ffn1, self.dropout)

        # ffn2
        ffn2 = contrib.layers.fully_connected(inputs=ffn1, num_outputs=128, activation_fn=tf.nn.relu)
        ffn2 = tf.nn.dropout(ffn2, self.dropout)

        # ffn3
        ffn3 = contrib.layers.fully_connected(inputs=ffn2, num_outputs=256, activation_fn=tf.nn.relu)
        ffn3 = tf.nn.dropout(ffn3, self.dropout)

        # ffn4
        ffn4 = contrib.layers.fully_connected(inputs=ffn3, num_outputs=512, activation_fn=tf.nn.relu)
        ffn4 = tf.nn.dropout(ffn4, self.dropout)

        # output layer
        out = contrib.layers.fully_connected(inputs=ffn4, num_outputs=self.num_class, activation_fn=None)

        return out

    def loss(model_out, y):
        logit = tf.identity(model_out, name='logits')

        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logit, labels=y))

        return cost

    def optimizer(cost)
        optim = tf.train.AdamOptimizer(learning_rate=self.lr).minimize(cost)

        return optim

    def accuracy(logits):
        correct_pred = tf.equal(tf.argmax(logits, 1), tf.argmax(y, 1))
        acc = tf.reduce_mean(tf.cast(correct_pred, tf.float32), name='accuracy')

        return acc
 
    def train_neural_network(session, optimizer, dropout_p, feature_batch, label_batch):
        session.run(optimizer, feed_dict={x: feature_batch, y: label_batch, dropout_p: dropout_p})

    def print_stats(session, feature_batch, label_batch, cost, accuracy):
        loss = sess.run(cost, feed_dict={x: feature_batch, y: label_batch, dropout_p: 1.})
        valid_acc = sess.run(accuracy, feed_dict={x: valid_features, y: valid_labels, dropout_p: 1.})

        print('Loss: {:>10.4f} Validation Accuracy: {:.6f}'.format(loss, valid_acc))
