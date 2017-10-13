#!/usr/bin/python3

import time
import zmq
import sys
import numpy as np
from queue import Queue

port = 8887

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://192.168.2.82:%s"%port) #raspberry pi ip address

topicfilter=b""
socket.setsockopt(zmq.SUBSCRIBE,topicfilter)

while True:
	string = socket.recv()

	data = np.fromstring(string, dtype="int16")
#	data = cPicle.loads(string)
	print(data)
