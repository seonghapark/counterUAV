
wav_name='range_test2.wav'
wav_time=25

#option: drawing graph =0, draw_max,min = 1
option=0

python3 fft.py ${wav_name}
#wait $(jobs -l | awk '{print $2}')

case ${option} in
	0)
		python3 draw_graph.py ${wav_time}
		;;
	1)
		python3 max.py ${wav_time}
		python3 maxplot.py ${wav_time}
		;;
esac