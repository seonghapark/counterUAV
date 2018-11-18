import tensorflow as tf
import os
from os.path import isfile
import sys
import pickle
import numpy as np
import argparse
from datetime import datetime 
from feature_extract import FeatureParser
from train_layers import ConvNet

# experiment setting
FRAMES = 50
BANDS = 82
TRAINING_EPOCHS = 5000

FEATURE_SIZE = FRAMES * BANDS  # 60 X 41
NUM_CH = 1
BATCH_SIZE = 10
KERNEL_SIZE = 15
HIDDEN1 = 400
DEPTH = 20
LEARNING_RATE = 1e-6
NUM_CLASSES = 4

# path setting
PICKLE_FILE = 'pickle/audio_CNNdataset_rti'\
    + '_' + str(BANDS) + 'x' + str(FRAMES)\
    + '_fold.pickle'
PARENT_DIR = '../raw_data/data'
PLOT_DIR = '../../log_counterUAV/plot'


def main():
    tf.reset_default_graph()

    parent_dir = PARENT_DIR
    sub_dir = ['0', 'raw_1', 'raw_2', 'raw_3']

    parser = argparse.ArgumentParser(description='Set num. of layers and residual connection.')
    parser.add_argument('-l', '--nlayers', default='1', type=str, help='Integer for number of convolutional layers')
    parser.add_argument('-r', '--res_flag', default=False, type=bool, help='Flag for residual connection')
    parser.add_argument('-f', '--nfolds', default=5, type=int, help='Number of k in k-folds cross validation')
    args = parser.parse_args()

    print('Arguments:--------------',
            '\nNUM_LAYERS:', args.nlayers,
            '\nRES_FLAG:', args.res_flag, 
            '\nNFOLDS:', args.nfolds,
            '\n------------------------')
    f = FeatureParser()
    if not isfile(PICKLE_FILE):
        print('Parent directory:', parent_dir)
        print('Sub directory:', sub_dir)

        print('Parsing audio files...')
        print('Extracting features...')
        features, labels = f.extract_rti_features(parent_dir, sub_dir)
        # k-folding with k=6  
        print('K-folding the dataset... ')
        k_fold_dict = f.k_fold(features, labels, k=5, seed=2018)

        data = k_fold_dict

        with open(PICKLE_FILE, 'wb') as handle:
            print('Save:', PICKLE_FILE)        
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    else:
        print('Reading audio pickle file...')
        with open(PICKLE_FILE, 'rb') as handle:
            print('Read:', PICKLE_FILE)        
            data = pickle.load(handle)


    # tr_features and ts_features in k-fold fashion
    tr_features, tr_labels, ts_features, ts_labels = f.pick_dataset(data, 5, args.nfolds) 
    title = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')\
        + '_' + str(BANDS) + 'x' + str(FRAMES)\
        + '_' + str(TRAINING_EPOCHS)

    tr_features = tr_features.reshape((-1, BANDS, FRAMES, 1))
    ts_features = ts_features.reshape((-1, BANDS, FRAMES, 1))

    print('tr_features shape: ', tr_features.shape)
    print('tr_features: ', tr_features)
    print('ts_features: ', ts_features.shape)
        

    # print parameters
    print('Title: ',  title)

    print('[ Input Data ]')
    print('Fold #: ', args.nfolds)
    print('tr_features: ', tr_features.shape)
    print('tr_labels: ', tr_labels.shape)
    print('ts_features: ', ts_features.shape)
    print('ts_labels: ', ts_labels.shape)
    print('')

    print('[ Input Data Parameter ]')
    print('Bands: ', BANDS)
    print('Frames: ', FRAMES)
    print('Channels: ', NUM_CH)
    print('Feature size: ', FEATURE_SIZE)
    print('Classes: ', NUM_CLASSES)
    print('')

    print('[ Hyper-parameter ]')
    print('Training Epochs: ', TRAINING_EPOCHS)
    print('Batch size: ', BATCH_SIZE)
    print('Kernel size: ', KERNEL_SIZE)
    print('Hidden layers: ', HIDDEN1)
    print('Depth: ', DEPTH)
    print('Learning rate: ', LEARNING_RATE)
    print('')

    tr_labels = f.one_hot_encode(tr_labels)
    ts_labels = f.one_hot_encode(ts_labels)

    # Initialize the ConvNet model
    model = ConvNet(BANDS, NUM_CLASSES, LEARNING_RATE, FRAMES, BANDS, NUM_CH, BATCH_SIZE, KERNEL_SIZE, HIDDEN1, DEPTH, TRAINING_EPOCHS)
    # Dynamically determine number of layers and residual connection 
    model.train_layers(tr_features, tr_labels, ts_features, ts_labels, args.nlayers, resFlag=args.res_flag)

    '''
    if args.nlayers == '1':
        model.train_layers(tr_features, tr_labels, ts_features, ts_labels)
    elif args.nlayers == '2':
        model.train_two_layers(tr_features, tr_labels, ts_features, ts_labels)
    elif args.nlayers == '3':
        model.train_three_layers(tr_features, tr_labels, ts_features, ts_labels)
    else:
        model.train_layers(tr_features, tr_labels, ts_features, ts_labels)
    '''
    if model.figure is None:
        return
    else: 
        model.figure.savefig(os.path.join(PLOT_DIR, title + '.png'))

if __name__ == '__main__':
    main() 
