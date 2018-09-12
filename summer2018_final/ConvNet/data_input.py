""" Preprocess and augment the radar training data"""

import tensorflow as tf
import cv2
import os
from random import shuffle
from tqdm import tqdm


IMG_SIZE = 30 #radar data image will be 30 x 30; any changes to the data dimension can be addressed by changing IMG_SIZE

NUM_CLASSES = 4
TRAIN_DIR = '~/counterUAV/summer2018_final/ConvNet'

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
    else #Others
        one_hot_list[3] = 1

    return one_hot_list

def create_train_data():
    training_data = []
    for img in tqdm(os.listdir(TRAIN_DIR)):
        label = label_img(img)
        path = os.path.join(TRAIN_DIR, img)

        #data preprocessing (gray scale, edge detection, etc.)
       
def create_test_data(): 
