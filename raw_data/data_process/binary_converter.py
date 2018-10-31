#! /usr/lib/python3
import numpy as np
import sys
from scipy.fftpack import fft
from scipy.io import wavfile
import librosa
import os

class RadarBinaryParser():
    def __init__(self, raw_data, sr=5862):
        self.raw_data = raw_data
        self.sr = sr
        self.sync = None
        self.data = None

    '''get sync, data and headers from text binary file.
    '''
    def parse(self):
        data = bytearray(self.raw_data)
        # print(len(data))
        # parse the sync and data signal in bytearray
        if len(data) < 2:
            return None, None
        if (data[0] >> 6) > 0:
            del data[:1]
        if len(data) % 2 == 1:
            del data[-1:]

        values = []
        sync = []
        for index in range(0, len(data), 2):
            high = data[index] & 0x1F
            low = data[index + 1] & 0x1F
            values.append(high << 5 | low)  
            sync.append(True if (data[index] >> 5) == 1 else False)

        self.sync = np.array(sync)
        self.data = np.array(values)
        
        # print(self.sync, self.data, len(self.sync), len(self.data))
        return self.sync, self.data


def main():
    # read binary file
    print('Read file: ', sys.argv[1])
    src_path = sys.argv[1]
    src_basename = os.path.basename(src_path)

    try:
        file = open(src_path, "rb")
        read_data = file.read()
        filename = os.path.splitext(src_basename)[0]  # get file name
    except (KeyboardInterrupt, Exception) as ex:
        print('Unable to read file: ', file)
        print(ex)
        return
    finally:
        file.close()

    # parse text binary file
    parser = RadarBinaryParser(read_data, sr=5862)
    sync, data = parser.parse()

    # stacking audio data 
    print('sync: ', sync, ' data: ', data)
    print('get: ', len(sync), len(data))
    audio = np.vstack((sync, data))
    # print(audio.shape[1])

    # write a wav file 
    print('audio: ', audio)
    wavfile.write(filename + ".wav", parser.sr, audio.T.astype(np.int16))
    print('Finish to read... ')


if __name__ == '__main__':  
    main()