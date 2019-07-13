7-12
1. 머신러닝 공부중.. (RNN)
2. 텐서플로우 환경설정 완료
3. Urban_Sound_Classification_using_NN 코드 분석중
4. 나만의 RNN 모델 구상중
(1초마다 데이터가 들어오고(n초 동안), 이 데이터는 10비트 길이의 데이터가 5862개씩 들어 오는 것이다.
--> 이를 input dimension을 5862으로 두고, n초를 n개의 sequence로 봐서 처리할 수 있지 않을까??)
5. raw data를 파싱하여 rnn 모델에 넣을 수 있는 numpy 파일을 만드는 코드 작성중 (RNN-parse.ipynb)
6. parse() 함수는 data[index]가 00으로 시작하고 data[index+1]이 11로 시작하는 것을 전제로 작성되었는데, 이 규칙을 벗어나는 현상 발견. (parse()함수 수정으로 해결)



