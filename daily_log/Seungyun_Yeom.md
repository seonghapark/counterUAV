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
1. RNN 모듈을 ROS 노드에 연결하기 위한 사전 작업 
* * *
