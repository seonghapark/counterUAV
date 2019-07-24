Requirements
=======

## 1.fake radar

- fake data sender
데이터 타입 정의 필요
기존에 존재하는 rawdata를 읽어들이는 부분 필요
읽어들인 rawdata를 msg로 publisher로 구현 필요

## 2.Counter UAV

- Data reciever node
subscriber로써 대기하면서 보내주는 msg를 수신
(예비)수신결과 출력

- ### 2.1 기존 리얼타임 코드 재사용 부분
  - rabbitmq 로컬 설치 시도 필요

  - #### 2.1.1. Analyzer node
  - #### 2.1.2. Visualizing node


- ### 2.2 Web connection
  - 여러 후보 존재 
  - #### 2.2.1. web video server + web server engine
  - #### 2.2.2. ros bridge + flask(web engines)
    - flask와 ros 연결한 관련 라이브러리 있는지 확인해보고 있으면 구현해보기

## 3. RNN Decision node

## 4. Priority

> 1. fake data sender node 만들기
> 2. data reciever node 만들기
> 3. 웹 통신 예제 해보기
> 4. 리얼타임 코드 노드화