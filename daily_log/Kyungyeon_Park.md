# Daily log of Kyungyeon Park

## 2019-09-04 ~ 2019-09-06

### 2019-09-04
- 구체적인 주제 회의
  - 센서 개발
  - 웹 인터페이스
  - 데이터 전송 딜레이 최적화
  - ROS 및 웹 연동
  
### 2019-09-05
- 논문 읽기
  - Realization of an Autonomous, Air-to-Air Counter Unmanned Aerial System (CUAS)
  
### 2019-09-06
- `counterUAV` 안의 `README.md` 수정
  - ros 설치 방법이 구체적이지 않아 조금 더 구체적으로 작성해 놓음
- `RNN.py` 수정
  - `/home/project/counterUAV/ROS_system/catkin_ws/src/ros_counteruav/scripts` 안의 `RNN.py`를 수정함
  - `time_list.npy`가 `RNN.py`에서 인식이 되지 않아 상대경로에서 절대경로로 바꿔 놓음
- `ROS_system` 파일 실행
  - `$ rosrun ros_counteruav scripts/start.sh` 명령어를 통해 `ROS_system`를 실행시켜 봄
  - [결과](https://ibb.co/0hWLjYv) >> 이렇게 뜨는게 맞는지 모르겠음

<br/>

## 2019-09-09 ~ 2019-09-13

### 2019-09-09
- `start.sh`안의 프로그램 실행 구조 파악
- `visualizer.py`, `data_analyzer.py`, `data_receiver.py`, `fake_data_sender.py`안의 코드들을 분석해봄
