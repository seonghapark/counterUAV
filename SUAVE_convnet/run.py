import tensorflow as tf
import pickle
import numpy as np
from feature_extract import FeatureParser
from train_layers import FeedForward
from os.path import isfile

NUM_CLASS=10
LEARNING_RATE=1e-3
PARENT_DIR='/media/jeonghwan/Seagate Expansion Drive/UrbanSound8K/audio'

def main():
    parent_dir = PARENT_DIR
    sub_dir = ['fold1', 'fold2', 'fold3', 'fold4', 'fold5', 'fold6', 'fold7', 'fold8', 'fold9', 'fold10']

    if not isfile('audio_dataset.pickle'):
        f = FeatureParser()
        print('Parsing audio files...')
        print('Extracting features...')
        features, labels = f.parse_audio_files(parent_dir, sub_dir)
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

        with open('audio_dataset.pickle', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    else:
        with open('audio_dataset.pickle', 'rb') as handle:
            data = pickle.load(handle)

    tf.reset_default_graph()

    with tf.Session() as sess:
        print('Shape of test_x:{}'.format(sess.run(tf.shape(data['ts_features']))))

    print('TRAIN_X:{}\nTEST_X:{}'.format(data['tr_features'], data['ts_features']))
    #print('FEATURE SHAPE:{}'.format(data['tr_features'].shape[1]))

    # Initialize the feed-forward model
    model = FeedForward(data['tr_features'].shape[1], NUM_CLASS, LEARNING_RATE)
    model.train_layers(data['tr_features'], data['tr_labels'], data['ts_features'], data['ts_labels'])


if __name__ == '__main__':
    main()
