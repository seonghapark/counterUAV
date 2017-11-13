set initial value
===============
.wav -> fft -> noise cancel -> find max, find initial -> draw max graph
-
## set initial value 
처음으로 나오는 10m 이상의 값을 initial value로 설정

## "script.sh"
노이즈 캔슬링 후 max값의 그래프를 그려줌
## "fft.py" 
wav파일의 데이터를 fft변환, dbv변환 후 결과를 time_ndarray.txt, val_ndarray.txt에 저장
## "max.py" 
time_ndarray.txt, val_ndarray.txt를 읽어와 노이즈를 제거한 후 각 시간에 대해서 max값의 index를 .txt파일에 저장
initial value를 찾아서 출력
## "maxplot.py" 
max.py에서 만든 .txt를 이용하여 (시간, max값의 index) 그래프를 그림

