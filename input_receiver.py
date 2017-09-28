#!/usr/bin/python3

import time
import zmq
import sys
import numpy as np
from queue import Queue

port = 8887

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:%s"%port)

topicfilter=b""
socket.setsockopt(zmq.SUBSCRIBE,topicfilter)

while True:
	string = socket.recv()

	data = np.fromstring(string, dtype="int16")
#	data = cPicle.loads(string)
	print(data)
