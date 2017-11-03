noise cancelling
===============
.wav -> noise cancel -> find max -> draw max graph
-
## 노이즈 캔슬링 방법
데이터 중에서 2.5m 아래에 있는 데이터를 모두 무시한다.

## "script.sh" 
노이즈 캔슬링 후 max값의 그래프를 그려줌
## "fft.py" 
wav파일의 데이터를 fft변환, dbv변환 후 결과를 time_ndarray.txt, val_ndarray.txt에 저장
## "max.py" 
time_ndarray.txt, val_ndarray.txt를 읽어와 노이즈를 제거한 후 각 시간에 대해서 max값의 index를 .txt파일에 저장
## "maxplot.py" 
max.py에서 만든 .txt를 이용하여 (시간, max값의 index) 그래프를 그림

##range_test2_result.jpg
'range_test2.wav'파일을 이용하여 얻은 결과
