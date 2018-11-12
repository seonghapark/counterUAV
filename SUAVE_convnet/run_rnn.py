import tensorflow as tf
import os
from os.path import isfile
import pickle
import numpy as np
from feature_extract import FeatureParser
from train_layers import RecurrentNet

FRAMES = 41
BANDS = 60
HOP_LENGTH = 512
TRAINING_EPOCHS = 10000

FEATURE_SIZE = BANDS * FRAMES  # 60 X 41
BATCH_SIZE = 10
KERNEL_SIZE = 30
HIDDEN1 = 300
DEPTH = 20

PICKLE_FILE = './pickle/audio_CNNdataset'\
    + '_' + str(BANDS) + 'x' + str(FRAMES)\
    + '_' + str(HOP_LENGTH)\
    + '_fold.pickle'
PARENT_DIR = '../raw_data/data'
LEARNING_RATE = 1e-6
NUM_CLASSES = 4

def main():
    tf.reset_default_graph()

    parent_dir = PARENT_DIR
    sub_dir = ['0', '1', '2', '3', 'raw_1', 'raw_2', 'raw_3']

    print('PATH:', os.path.join(parent_dir, sub_dir[0]))

    f = FeatureParser()
    if not isfile(PICKLE_FILE):
        print('Parsing audio files...')
        print('Extracting features...')
        features, labels = f.extract_CNNfeature(parent_dir, sub_dir, bands=BANDS, frames=FRAMES, hop_length=HOP_LENGTH)

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

    # tr_features and ts_features in k-fold fashion
    tr_features, tr_labels, ts_features, ts_labels = f.pick_dataset(data, 6, 6)  

    tr_features = tr_features[:, :, :, 0]
    ts_features = ts_features[:, :, :, 0]

    # set features shapeS
    np.transpose(tr_features, (0, 2, 1))
    np.transpose(ts_features, (0, 2, 1))

    print('tr_features: ', tr_features.shape)
    print('tr_labels: ', tr_labels.shape)
    print('ts_features: ', ts_features.shape)
    print('ts_labels: ', ts_labels.shape)

    tr_labels = f.one_hot_encode(tr_labels)
    ts_labels = f.one_hot_encode(ts_labels)

    # Initialize the ConvNet model
    model = RecurrentNet(tr_features.shape[2], tr_features.shape[1], NUM_CLASSES, LEARNING_RATE, BATCH_SIZE, HIDDEN1, TRAINING_EPOCHS)
    model.train_layers(tr_features, tr_labels, ts_features, ts_labels)

if __name__ == '__main__':
    main() 
