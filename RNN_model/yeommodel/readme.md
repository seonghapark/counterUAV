5sec_slice_wav_data<t>: training, testing data 모음 폴더이다. cut_wav(Jiny_yeom) 파이썬 코드를 실행시킨 결과이다.<br>
5sec_slice_wav_data_backup<t>: 아무런 변환을 가하지 않은 5초 wav 파일들 백업<br>
5sec_slice_wav_data_noise<t>: 노이즈 추가한 5초 wav 파일들 백업<br>
5sec_slice_wav_data_time_stretch<t>: 시간 변환한 5초 wav 파일들 백업<br>
5sec_slice_wav_data_double_drone<t>: 드론만 파일 갯수를 2배로 늘린 5초 wav파일 백업<br>
<br>
all_wav<t>: 각 라벨들을 모두 이어붙힌 wav파일<br>
all_wav_backup<t>: 각 라벨들을 모두 이어붙힌 wav파일 백업<br>
<br>
binary_convert_wav<t>: binary_converter.py에 의해 binary.txt 파일이 wav 파일로 변환한 파일들<br>
binary_convert_wav_backup<t>: 백업 파일<br>

cut_wav<t>: 해당 라벨이 잡힌 구간(rnn_label.txt참조)별로 잘라서 저장. cut_wav(Jiny_yeom) 파이썬 코드를 실행시킨 결과이다.<br>
cut_wav_noise_stretch: data에 augmentation을 하고 라벨이 잡힌 구간을 잘라 저장한 wav파일들<br>
<br>
graph<t>: 각 입력 데이터들 별로 결과(그래프(.jpg), cost & 정확도(try.txt))를 저장하고 있다.<br>
<br>
rawdata<t>: binary txt파일이 저장되어 있다.<br>
rawdata_backup<t>: rawdata 백업<br>
rawdata_onlydrone<t>: 드론데이터만 5초간격이 아니라 2초 간격(cut_wav(Jiny_yeom)_2sec.py)으로 자르기 위해 따로 저장한 파일들<br>
<br>
rnn_data01<t>: 앞데이터들 trainig, testing data들이 들어있다.<br>
rnn_data02<t>: 뒤데이터들 trainig, testing data들이 들어있다.<br>
rnn_data03<t>: 랜덤데이터들 trainig, testing data들이 들어있다.<br>
rnn_data05<t>: 각 라벨별로 5초씩 나누지 않고 한꺼번에 이어붙힌 wav파일들의 trainig, testing data들이 들어있다.<br>
rnn_data06<t>: 05폴더의 데이터들의 시간 길이를 맞춘 wav 파일들의 trainig, testing data들이 들어있다.<br>
rnn_data08<t>: 앞데이터들 trainig, testing data들이 들어있다.<br>
rnn_data09<t>: 변조 데이터들 이랑 원본 데이터 다 섞음(자른 시간이 다름, 5초 1.2배 늘린것은 6초짜리 wav 파일이다.) 테스트 데이터는 원본 데이터들만 존재한다(잡음x 시간조절x) trainig, testing data들이 들어있다.<br>
rnn_data10_onelabel<t>: 1 라벨만 확인하기 위한 trainig, testing data들이 들어있다.<br>
<br>
rnn_graph_save<t>: RNN.py를 실행하면 RNN 모델을 저장하게 되는데 이곳에 저장된다.(수동으로 rnn_model_save에 백업해놓아야 한다.)<br>
rnn_model_save<t>: rnn_graph_save에 입력 데이터 별로 모델을 저장함<br>
<br>
slice_wav_data<t>: rnn_data01~10까지의 training, testing 폴더를 복사 붙혀넣기 하면 트레이닝과 테스트를 진행할 수 있다.(RNN.py에서 참조 한다.)<br>
<br>
5sec_wav_check.py<t>: 파일 크기가 5초가 맞는지 확인하기 위한 파이썬 코드<br>
binary_converter.py<t>: binary txt 파일을 wav 파일로 변환하기 위한 코드<br>
cut_wav(Jiny_yeom)_2sec_interval.py<t>: 드론 데이터를 늘리기 위해 2초 간격으로 자르기 위한 코드(단 raw_data 폴더에 rawdata_onlydrone 안에 파일들이 들어가 있어야한다. 5초짜리 wav파일이 만들어진다.)<br>
cut_wav(Jiny_yeom)_5sec_interval.py<t>: 드론 데이터를 늘리기 위해 5초 간격으로 자르기 위한 코드(5초짜리 wav파일이 만들어진다.)<br>
cut_wav(Jiny_yeom)_2sec_stretched.py<t>: 시간 변환이 들어간 데이터를 자르기 위한 코드(5*늘린길이 짜리 wav파일이 만들어진다.)
<br>
<br>
data_list_sec.npy<t>: raw 데이터를 list 형태로 저장함<br>
label_list.npy<t>: 몇 번째 파일이 어떤 라벨인지 list 형태로 저장함 (cut_wav(Jiny_yeom)*.py에서 사용한다.)<br>
time_list.npy<t>: 몇초부터 몇초까지 물체가 잡혔는지 list 형태로 저장함(cut_wav(Jiny_yeom)*.py에서 사용한다.)<br>
<br>
RNN.py<t>: RNN training, testing 파일이다. 논문에 작성된 코드이다.<br>
RNN_GRU.py<t>: LSTMCell 에서 GRUCell 로 바꾸어 실험해본 코드이다.<br>
<br>
show_graph.py<t>: try.txt 파일을 참고하여 정확도와 cost 그래프를 그려준다. (try.txt는 graph 폴더에 저장되어 있다.)<br>
<br>



