""" Preprocess and augment the radar training data"""

import tensorflow as tf
import cv2
import os
import pickle
from random import shuffle
from tqdm import tqdm


IMG_SIZE = 30 #radar data image will be 30 x 30; any changes to the data dimension can be addressed by changing IMG_SIZE

TRAIN_DIR = '~/counterUAV/summer2018_final/ConvNet/Train_Data'

def label_img(img, num_classes):
    #person.2283.png
    word_label = img.split('.')[-3]
    one_hot_list = [0] * num_classes
    if word_label == 'person':
        one_hot_list[0] = 1
    elif word_label == 'car':
        one_hot_list[1] = 1
    elif word_label = 'tree':
        one_hot_list[2] = 1
    else: #Others
        one_hot_list[3] = 1

    return one_hot_list

def create_train_data():
    training_data = []
    for img in tqdm(os.listdir(TRAIN_DIR)):
        label = label_img(img)
        path = os.path.join(TRAIN_DIR, img)

        #data preprocessing (gray scale, edge detection, etc.)
       
def create_test_data():

def DataLoader(batch_idx, batch_size):
# For loading data for the RadarNet model
    if os.path.exists(TRAIN_DIR):
        try:
            with open(TRAIN_DIR + '/data_batch_' + str(batch_idx), mode='rb') as file:
                batch = pickle.load(file, encoding='latin1')

            features = batch['data'].reshape((len(batch['data']), 3, IMG_SIZE, IMG_SIZE)).transpose(0, 2, 3, 1)
            labels = batch['labels']

        except IOError:
            print('Failed to read from {}'.format(TRAIN_DIR))

    return batch_features, batch_label
