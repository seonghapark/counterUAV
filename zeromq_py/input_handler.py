#!/usr/bin/python3

import time
import zmq
from queue import Queue

class Source(object):
    def __init__(self):
        pass

    def get_chunk(self):
        raise RuntimeError('get_chunk needs to be defined')

try:
    import spidev

    class AudioSPISource(Source):
        def __init__(self):
            super()
            self.open()

        def open(self):
            pass

        def get_chunk(self):
            pass

except:
    print(' [x] spidev is not available; only in raspberry PI')


from scipy.io import wavfile

class DummySource(Source):
    def __init__(self, file_name):
        super()
        self.fs, self.data = wavfile.read(file_name)
        self.data = self.data.T
        self.chunk_size = 44100
        self.count = 1
        self.pause = 1

    def get_chunk(self):
        if self.count + self.chunk_size < self.data.shape[1]:
            data = self.data[:,self.count:self.count + self.chunk_size]
            self.count += self.chunk_size
            time.sleep(self.pause)
            print(data.shape)
            return data.tostring()
        else:
            return None

class DataPublisher(object):
    def __init__(self, source):
        self.port = 8887 # port number
        self.zmq = zmq.Context()
        self.topic = b'Audio'
        self.source = source
        self.socket = None

    def open(self):
        self.socket = self.zmq.socket(zmq.PUB)
        self.socket.bind("tcp://wlan0:%s" % self.port) #tcp data transfer

    def close(self):
        if not self.socket.closed:
            self.socket.close()

    def run(self):
        if self.socket.closed:
            self.open()

        while True:
            chunk = self.source.get_chunk()
            if chunk is None:
                break
            print('Sending data... Length:%d' % (len(chunk),))
            self.socket.send(chunk)

print('Start handler....')
handler = DataPublisher(DummySource('./range_test2.wav'))
handler.open()
handler.run()
print('Done.')
