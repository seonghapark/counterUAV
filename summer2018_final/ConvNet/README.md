# Counter UAV Radar project - Argonne National Labs.

## Convolutional Neural Network (CNN) model for radar data processing & classification

### Using Tensorflow as the project's basic API


1D frequency data is converted into a 2D image data to be trained by our convolutional neural network.


## Following is the list of steps we are taking to post-process the received data and classify them using our trained network


	1. Pre-processing & Data augmentation
	2. Feed the training data into the neural network
	3. Backpropagate using optimization algorithms provided by Tensorflow (i.e. Adagrad, RMSProp)
	4. Continue training until the loss is reasonably low and performance shows a promising result
	5. Use the validation data to check for overfitting
	6. Use the test data to evaluate the model


