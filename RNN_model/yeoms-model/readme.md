# File Explanation

## File execution order
1. binary_converter.py(using rawdata directory & make .npy files and binary_convert_wav directory)<br>
2. cut_wav(Jiny_yeom).py(using binary_convery_wav directory & make cut_wav directory and 5sec_slice_wav_data directory)<br>
3. RNN.py(using for_rnn directory & make rnn_graph_save directory)<br>

## what are they do?
1. 5sec_slice_wave_data: 라벨링이 끝난 wav 파일을 RNN 모델에 입력으로 넣기 위해 5초씩 잘라 wav파일로 저장함
2. binary_convert_wav: Raw data(.txt) 상태로 있었던 파일을 wav 파일로 변환하여 저장함
3. cut_wav: 물체가 있는 부분만 잘라서(rnn_label.txt파일에 있는 시간을 참조) 저장하고 물체가 없는 부분은 other로 따로 wav파일로 저장함
4. for_rnn: 5sec_slice_wave_data 디렉토리에 있는 5초짜리 wav 파일을 수작업으로 training과 testing 데이터로 나누어 저장함
5. old_backup: 과거 실험했던 파일들
6. rawdata: binary.txt 파일들
7. rnn_graph_save: rnn.py 에서 생성한 모델들을 저장함
8. rnn_data1 2 3: 트레이닝, 테스트 데이터를 앞부분만(1) 뒷부분만(2) 랜덤하게(3) 뽑은 파일(정확도가 데이터에 따라 들쭉날쭉이라 3가지로 나누어 학습)
* * *
