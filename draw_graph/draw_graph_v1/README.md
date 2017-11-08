graph
===============
.wav -> color graph or min,max graph
-
## "script.sh" 
옵션에 따라 그래프가 생성됨
## "input_handler.py" 
.wav을 1초씩 끊어서 zmq로 송신함
## "fft.py" 
zmq로 수신한 데이터를 fft변환, dbv변환 후 결과를 time_ndarray.txt, val_ndarray.txt에 저장
## "draw_graph.py" 
time_ndarray.txt, val_ndarray.txt를 읽어와 색으로 표현한 그래프를 그림
## "minmaxavg.py" 
time_ndarray.txt, val_ndarray.txt를 읽어와 각 시간에 대해서 min, max, avg값과 min값의 index, max값의 index를 .txt파일에 저장
## "minmaxplot.py" 
minmaxavg.py에서 만든 .txt를 이용하여 (시간, 최솟값) 그래프와 (시간, 최댓값) 그래프를 그림