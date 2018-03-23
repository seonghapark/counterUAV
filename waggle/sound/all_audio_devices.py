import pyaudio

audio = pyaudio.PyAudio()

all_num = audio.get_device_count()
print(all_num)

#for i in range(all_num):
#    print(audio.get_device_info_by_index(i))

print(audio.get_device_info_by_index(9))



