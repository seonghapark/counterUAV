import pyaudio
import wave
import math

import audioop
import numpy as np

import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()


# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=9)
#stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# def read_audio():
print ("recording...")
frames = []
audioop_frames = b''

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    audioop_frames += data
print ("finished recording")

# stop Recording
#stream.stop_stream()
#stream.close()
#audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

fs, data = wavfile.read(WAVE_OUTPUT_FILENAME)
a = data.T
b = [(ele/2**16.)*2-1 for ele in a]
c = fft(b)
d = len(c)/2
print(type(c), c[:10])

plt.plot(abs(c[:(d-1)]), 'r')
plt.show()

#     return audioop_frames
#
# if __name__ == "__main__":
#
#     while True:
#         try:
#             audioop_frames = read_audio()
#             audio_power_in_watts = audioop.rms(audioop_frames, 2)
#             watts_to_dBm = 10*math.log10(audio_power_in_watts) + 30
#             print(watts_to_dBm)
#
#             fs, data = wavefile.read(WAVE_OUTPUT_FILENAME
#             print(type(data), len(data))
#
#         except (KeyboardInterrupt):
#             print("Keyboard Interruption occurred")
#             stream.stop_stream()
#             stream.close()
#             audio.terminate()
#             break
#         except:
#             stream.stop_stream()
#             stream.close()
#             audio.terminate()
#             break
