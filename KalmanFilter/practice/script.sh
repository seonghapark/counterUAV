
wav_name='range_test2.wav'
wav_time=25

python3 fft.py ${wav_name}
python3 max.py ${wav_time}
python3 basic_kalman.py ${wav_time}
python3 maxplot.py ${wav_time}