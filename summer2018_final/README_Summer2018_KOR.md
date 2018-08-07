# Counter UAV - Summer 2018


## Folders
RealTime 폴더에는 실시간으로 받은 데이터 또는 txt 파일 데이터를 처리하는 코드들이 있고,
WaveFile 폴더에는 range_test2.wav 데이터를 처리하는 코드가 있습니다.
코드들 이름을 바꿨는데 데이터 처리 순서를 번호로 매겨서 이름을 바꿨습니다.


## 1. Read Data
RealTime에서 txt 파일을 11025바이트 단위(1초)로 파싱한다. 


## 2. FFT


## 3. Threshold
FFT에서 받아온 데이터(50,1764) 중 Threshold(임계값)을 기준으로 데이터를 추출한 후 특정 시간의 평균을 데이터(1차원 배열)로 전송한다.
RealTime에서는 Amplitude를 -9이상으로 하였고, 더 큰 값으로 수정할까 고민중입니다.
WaveFile에서는 Amplitude를 -12이상, Distance를 24이상으로 하였다.


## 4. Filtering
### Kalman Filter (2)
http://www0.cs.ucl.ac.uk/staff/gridgway/kalman/kalman_example/Kalman_Example.html

### Extended Filter

### Particle Filter (4)
https://github.com/vinaykumarhs2020/lane_detection

## 5. Drawing
Threshold(1), Kalman Filter(2), Particle Filter(4)의 결과를 점으로 나타내었다.
기존 코드의 pcolormesh를 scatter로 바꾸었다.
WaveFile에 보면 full이라는 이름이 들어간 파일이 있는데 그 파일은 인풋 데이터 전체를 그린 것 입니다.