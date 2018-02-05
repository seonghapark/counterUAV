import zmq
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:8887") #tcp data transfer

data0 = np.array([1])
data1 = np.array([1.0, 0.2, 0.3])
data2 = np.array([1.0, 2.0, 3.0])
while True:
    socket.send(data0)
    socket.send(data1)
    socket.send(data2)

