import tensorflow as tf
import os
from os.path import isfile
import pickle
import numpy as np
from feature_extract import FeatureParser
from train_layers import ConvNet

FRAMES = 41
BANDS = 60

FEATURE_SIZE = 2460 # 60 X 41
NUM_CH = 2
BATCH_SIZE = 50
KERNEL_SIZE = 30
HIDDEN1 = 500
DEPTH = 20

PARENT_DIR='../raw_data'
LEARNING_RATE=1e-3
NUM_CLASSES = 4

def main():
    tf.reset_default_graph()

    parent_dir = PARENT_DIR
    sub_dir = ''
    #sub_dir = ['fold1', 'fold2', 'fold3', 'fold4', 'fold5', 'fold6', 'fold7', 'fold8', 'fold9', 'fold10']

    print('PATH:', os.path.join(parent_dir, sub_dir[0]))

    if not isfile('audio_CNNdataset.pickle'):
        f = FeatureParser()
        print('Parsing audio files...')
        print('Extracting features...')
        features, labels = f.extract_CNNfeature(parent_dir, sub_dir)
        labels = f.one_hot_encode(labels)

        tr_ts_split = np.random.rand(len(features)) < 0.70
        train_x = features[tr_ts_split]
        train_y = features[tr_ts_split]
        test_x = features[~tr_ts_split]
        test_y = features[~tr_ts_split]

        data = {'tr_features': train_x,
                     'tr_labels': train_y,
                     'ts_features': test_x,
                     'ts_labels': test_y}

        with open('audio_CNNdataset.pickle', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    else:
        with open('audio_CNNdataset.pickle', 'rb') as handle:
            data = pickle.load(handle)

#    with tf.Session() as sess:
#        print('Shape of train_x:{}'.format(sess.run(tf.shape(data['tr_features']))))

    print('TRAIN_X:{}\nTEST_X:{}'.format(data['tr_features'], data['ts_features']))
    #print('FEATURE_SHAPE:{}'.format(features.shape[1]))

    # Initialize the ConvNet model
    model = ConvNet(data['tr_features'].shape[1], NUM_CLASSES, LEARNING_RATE, FRAMES, BANDS, NUM_CH, BATCH_SIZE, KERNEL_SIZE, HIDDEN1, DEPTH) 
    model.train_layers(data['tr_features'], data['tr_labels'], data['ts_features'], data['ts_labels'])

if __name__ == '__main__':
    main() 
