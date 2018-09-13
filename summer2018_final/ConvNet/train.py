import tensorflow as tf
from model import RadarNet
from data_input import DataLoader

NUM_CLASSES = 4

def train():

    if __name__ == '__main__':
        opt = {}
        opt['batch_size'] = 5
        opt['num_class'] = NUM_CLASSES
        opt['learning_rate'] = 1e-3
        opt['dropout_p'] = 0.5
        opt['epoch'] = 10 


    print("Training...")
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for epoch in range(opt['epoch']):
            for i in range(1, opt['batch_size'] + 1):
               for batch_features, batch_labels in DataLoader(i, batch_size): 
