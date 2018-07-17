
wav_name='../range_test2.wav'
wav_time=10

printf "Enter option(0,1,2)\n0) draw color graph\n1) draw max graph\n2) after noisecancelling and kf graph\n(option[Enter])\n"
read option

case ${option} in
	0)
		python3 fft.py ${wav_name}
		python3 draw_graph.py ${wav_time}
		;;
	1)
		python3 fft.py ${wav_name}
		python3 max.py ${wav_time}
		python3 maxplot.py ${wav_time}
		;;
	2)
		python3 fft.py ${wav_name}
		python3 max.py ${wav_time}
		printf "Enter initial_time and initial_distance above(initial_time[Enter]initial_distance[Enter])\n"
		read initial_time
		read initial_distance
		python3 newplot.py ${wav_time} ${initial_time} ${initial_distance}
		;;
esac
