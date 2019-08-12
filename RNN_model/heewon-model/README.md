### 코드 실행 순서
1. RNN-Model-wav-4 파일실행
2. make_data 함수의 wav_file_path_training = 'C://slice_wav_data/training/'' 부분에 트레이닝 데이터 경로 설정
3. 'wav_file_path_test = 'C://slice_wav_data/testing/' ' 부분에 테스팅 데이터 경로 설정

### 트레이닝 시킬 시에는
1. m1 = CUAV_Model()
2. m1.make_data()
3. m1.graph_setting()
4. m1.training()
순서대로 실행.
이 경우에는 100회 epoch마다 save_network 함수에 정의된 경로로 체크포인트 저장

### 트레이닝 완료후 예측 값을 만들 때에는
1. m1 = CUAV_Model()
2. m1.graph_setting()
3. m1.restore_graph(1200)
순서대로 실행. 3번의 m1.restore_graph 함수에 넣은 파라미터에 해당하는 epoch으로 그래프가 복원됨
이 후에 predict() 함수를 사용하면 저장된 그래프 대로 실행됨

### matplotlib를 이용하여 그래프 그리기
1. 앞에서 트레이닝 시켰을때의 코드 전체를 Ctrl+A 하여 전체 복사하여 텍스트 파일에 저장
2. RNN-Graph-wav 파일 실행
3. f = open() 부분에 1에서 만든 텍스트 파일 경로 설정
순서대로 실행
cost 그래프, accuracy 그래프, 최저 cost, 최대 accuracy값을 알 수 있다
