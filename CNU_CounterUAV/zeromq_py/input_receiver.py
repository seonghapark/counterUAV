#!/usr/bin/python3

import zmq
import numpy as np

port = 8887

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:%s"%port) #raspberry pi ip address

topicfilter=b""
socket.setsockopt(zmq.SUBSCRIBE,topicfilter)

while True:
	string = socket.recv()
	#print string

	data = np.fromstring(string, dtype="float")
	print(data)
