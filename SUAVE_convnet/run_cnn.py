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
BATCH_SIZE = 10
KERNEL_SIZE = 30
HIDDEN1 = 300
DEPTH = 20

PICKLE_FILE='audio_CNNdataset_fold.pickle'
PARENT_DIR='../experiment_data'
NUM_CLASSES = 4

def main():
    tf.reset_default_graph()

    parent_dir = PARENT_DIR
    sub_dir = ['fold1', 'fold2', 'fold3']

    print('PATH:', os.path.join(parent_dir, sub_dir[0]))

    f = FeatureParser()
    if not isfile(PICKLE_FILE):
        print('Parsing audio files...')
        print('Extracting features...')
        features, labels = f.extract_CNNfeature(parent_dir, sub_dir)

        # k-folding with k=6  
        k_fold_dict = f.k_fold(features, labels, k=6, seed=2018)

        data = k_fold_dict
        with open(PICKLE_FILE, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    else:
        with open(PICKLE_FILE, 'rb') as handle:
            data = pickle.load(handle)

#    with tf.Session() as sess:
#        print('Shape of train_x:{}'.format(sess.run(tf.shape(data['tr_features']))))

    #print('TRAIN_X:{}\nTEST_X:{}'.format(data['tr_features'], data['ts_features']))

    tr_features, tr_labels, ts_features, ts_labels = f.pick_dataset(data, 6, 6) #Tr_features and ts_features in k-fold fashion

    print('tr_features: ', tr_features.shape)
    print('tr_labels: ', tr_labels.shape)
    print('ts_features: ', ts_features.shape)
    print('ts_labels: ', ts_labels.shape)

    tr_labels = f.one_hot_encode(tr_labels)
    ts_labels = one_hot_encode(ts_labels)

    # Initialize the ConvNet model
    model = ConvNet(tr_features.shape[1], NUM_CLASSES, LEARNING_RATE, FRAMES, BANDS, NUM_CH, BATCH_SIZE, KERNEL_SIZE, HIDDEN1, DEPTH) 
    model.train_layers(tr_features, tr_labels, ts_features, ts_labels)

if __name__ == '__main__':
    main() 
