after_wav_data : wav 파일을 물체가 잡힌 구간만 이어붙힌 wav 파일 zip으로 묶어놓음
data : binary txt
wav_data : binary txt를 wav로 변환한 파일(이것으로 after_wav_data를 생성) zip으로 묶어놓음
cut_wav(Jiny_yeom).py : after_wav_data 를 생성하는 파이썬 프로그램 (원작자: 채진영, 수정 : 염)
Fail_RNN-parser.py : model MK1 실패작
Yeom_RNN-parser.py : rnn_label.txt를 보고 .npy 리스트를 생성
data_list_sec.npy : binary txt를 [[파일 하나],[[1초에 해당하는 5682개의 bit들],[2초],...],[],...] 이 형태로 다 이어붙힌 list
label_list.npy : 파일 순서대로 person, car, dron인지 저장한 list, 3번째 파일 label은 label_list[2]에 저장
time_list.npy : 물체가 있는 구간을 저장한 list, 3번째 파일 구간은 time_list[2] = [[시작,끝],[시작,끝],...]에 저장

* * *
