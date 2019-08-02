Seungyun Yeom
=============
염승윤 팀원의 일지입니다.
RNN 담당

## 2019-07-13~2019-07-19
### 2019-07-13(토)

1. [모두를 위한 머신러닝](https://www.youtube.com/playlist?list=PLlMkM4tgfjnLSOjrEJN31gZATbcj_MpUm) 수강완료
2. 생각한 RNN 모델에 대한 데이터 shape 결정 후 그에 맞는 raw_data 추출하는 코드 작성 중

### 2019-07-14(일)
1. 원하는 raw_data를 추출하는 코드에 버그가 발견되어 수정
2. 생각한 2가지 RNN 모델(레이블 별로 파일 1개만 선택하여 60초짜리 트레이닝 데이터로 학습) 중 정확도가 높은 모델로 여러개 파일로 만든 60초짜리 데이터로 트레이닝 할 예정 

### 2019-07-15(월)
1. 정확한 RNN 모듈을 만들기 위한 [모두를 위한 머신러닝](https://www.youtube.com/playlist?list=PLlMkM4tgfjnLSOjrEJN31gZATbcj_MpUm) RNN 부분 다시 공부
2. [realtime/2_analyzer.py](https://github.com/seonghapark/counterUAV/blob/sum2019/realtime/2_analyzer.py) 코드 분석

### 2019-07-16(화)
1. RNN 첫번째 모듈 완성
2. 푸리에 변환 학습

### 2019-07-17(수)
1. wav파일 중 유효한 데이터가 있는 구간만 잘라서 따로 wav파일로 저장하는 프로그램 완성
  결과는 after_data 와 after_data_normalize(amplitude normalization 함)

### 2019-07-18(목)
1. [Urban Sound](http://aqibsaeed.github.io/2016-09-03-urban-sound-classification-part-1/) 예제를 통해 새로운 모델 만들기 착수

### 2019-07-19(금)
1. 트레이닝 데이터를 각 라벨별 5초씩 잘라서 wav 파일에 저장하여 생성
2. [Urban Sound](http://aqibsaeed.github.io/2016-09-03-urban-sound-classification-part-1/)를 이용해 wav 파일 분석 코드를 만들어 트레이닝 

### 2019-07-23(화)
1. RNN 모듈을 ROS 노드에 연결하기 위한 사전 작업 (python 2에서 byte를 str로 인식하는 바람에 wav파일 생성에 필요한 bytearray를 못쓰고 있음)
2. RNN-Model_wav에 accuracy 계산 오류 수정(방금 트레이닝한 데이터로 정확도를 계산함 당연히 높게 나올 수 밖에 )

### 2019-07-24(수)
1. RNN 모듈을 ROS 노드에 연결하기 위한 사전 작업 완료(python 3버전 업데이트 이후 bytes를 str이 아닌 bytes로 인식시키는데 성공)

### 2019-07-25(목)
1. RNN모델을 ROS 노드에 넣어봤으나 결과가 많이 부정확하여 트레이닝 데이터를 여러 형태로 잘라봄(트레이닝 데이터 특징이 9개 추출되나 ROS로 넘어와서는 4개의 특징밖에 추출을 하지 못한다.)

### 2019-07-26(금)
1. 25일에 문제를 해결하느라 하루를 다 썼다. 진전이 없다.

### 2019-07-27(토)
여행 전 논문 작성을 위한 긴급 회의
1. 현재 melspecgram이랑 mfcc 두개의 특징으로 트레이닝 하고있는데 이게 왜 적합한지, 그렇지 않다면 그 이유 분석 + 다른 특징 넣어서도 머신러닝 해보기
2. 바이너리 파일로 학습했을때랑 wav파일로 바꿔서 했을때랑 차이점, 왜 더 잘되는지 이유 
3. 이 전에 CNN으로 했을때의 논문과 비교해서 이론적인 분석
4. 현재 raw_data를 RNN으로 분석했을 때 적합한 이유(CNN과 비교해서?)
5. 코스트 그래프랑 정확도 그래프가 계속 진동하는데 그 이유 --> + 이론적인 해결방안
6. others, person, drone, car를 정확하게 식별할 수 있는 feature가 무엇일까. 왜 식별이 되는 것일까.

-논문에 들어가야는 총 레퍼런스 개수는 최소 20개임. <br>
-각 항목별로 조사해서 정리하고, 레퍼런스 출처 명시
* * *
