# Sound classification using the Urban Sound Dataset

This repository contains codes that parse, extract and classify features from the dataset collected from our field experiments.

Deep neural network models are used to classify the frequency data in a .wav format according to the labeled classes.

## Deep Neural Networks

    Feed-forward neural net
    Convolutional neural net

## Train - Feed-forward neural net

    sh train.sh

## Train - Convolutional neural net

    sh train_cnn.sh

## Codes

    feature_extract.py: Extract features from .wav format files - read the comments for details

    train_layers.py: class FeedForward() is for Feed-forward neural network / class ConvNet() is for Convolutional neural network. Both models are implemented in Tensorflow framework. You must specify the hyperparameters at run.py (in case of FFN) or run_cnn.py (in case of CNN)
