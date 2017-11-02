graph
===============
.wav -> color graph or max graph
-
## "script.sh" 
옵션에 따라 그래프가 생성됨
## "fft.py" 
wav파일의 데이터를 fft변환, dbv변환 후 결과를 time_ndarray.txt, val_ndarray.txt에 저장
## "draw_graph.py" 
time_ndarray.txt, val_ndarray.txt를 읽어와 색으로 표현한 그래프를 그림
## "max.py" 
time_ndarray.txt, val_ndarray.txt를 읽어와 각 시간에 대해서 max값의 index를 .txt파일에 저장
## "maxplot.py" 
max.py에서 만든 .txt를 이용하여 (시간, max값의 index) 그래프를 그림

## v1과의 차이
* 'input_handler.py'와 'fft.py'를 'fft.py'로 합침
* 'draw_graph.py'의 데이터 처리과정을 (데이터를 저장하지 않음으로써)빠르게함
* 'minmaxavg.py'를 max값만 구하는 'max.py'로 바꿈
* 'minmaxplot.py'를 max값에 대한 그래프만 그리는 'maxplot.py'로 바꿈