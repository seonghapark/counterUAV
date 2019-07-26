# SoYeon Kim

김소연 팀원(ROS팀)의 일지입니다.

## 2019-07-13~2019-07-19

### 2019-07-13(토)

1. Git 기초사용법 학습
2. Ubuntu 및 ROS 설치
3. ROS 환경설정

### 2019-07-14(일) 과제
1. https://www.youtube.com/playlist?list=PLRG6WP3c31_VIFtFAxSke2NG_DumVZPgw 7강까지 학습
> 1 ~ 6강 수강. 7강 수강 못함. 내일 마저 수강

### 2019-07-15 (월)
1. 7강 수강 + 토픽/서비스 코드 작성과 수행
2. ROS 다이어그램 초안 완성


### 2019-07-16 (화)
* 2개의 세미나에 참여하는 시간이 길어 시간 투자가 적었음
1. ROS 강의 Chapter 8~10강 수강
> ROS 기초에 대해서 다룬 초반 부분과 중심적인 프로그래밍 강의를 제외하고 프로젝트에 필요한 부분은 9강(임베디드 시스템)이라고 판단하여 수강할 챕터를 조절.

2. 구상한 모델 구체화 및 노드 검색
> 재사용할 수 있는 노드들을 찾아보았을 때 웹 연결 부분이 가장 빨리 해결될 것으로 보여 관련 패키지와 연동 가능한 웹 서버 엔진 검색중
>- 웹 연결 부분에서 재사용할 수 있는 노드로 web_video_server라는 노드를 찾음. web_video_server는 HTTP를 통해 이미지, 비디오 토픽을 클라이언트에게 전달해주는 역할을 하는 노드. 웹에서 보여지는 데이터가 이미지인지, 비디오인지 정확히 설정해야 함.

> fake data sender node와 data receiver node 구현 시에 실제 안테나가 데이터를 송신할 때의 통신방법에 관한 학습 필요성 절감

### 2019-07-17 (수)
1. 회의 준비 및 진행
> 회의 준비를 하며 RNN팀과 진행상황을 공유하고, 회의 때 발표할 내용과 질문할 사항을 정리함.

2. ROS_MODEL 노드 구체화 순서 설정
> 1) fake data sender node 만들기
> 2) data reciever node 만들기
> 3) 웹 통신 예제 해보기
> 4) 리얼타임 코드 노드화
>-ROS_system/requirements.md 참조.

3. 바이너리 데이터를 전달하는 Publisher 코드 작성
> 과제로 바이너리 데이터를 전달하는 Publisher/Subscriber 구현 중에서 먼저 Publisher를 구현하고 있다. 나에게 더 익숙한 C++로 작성하고 있으며, 일단 raw_data에 있는 파일 하나를 읽어서 메세지에 담는 코드를 작성 중.


## 2019-07-22~2019-07-26

### 2019-07-22 (월)
1. analyzer 코드 + ROS 
> git에 올라와있는 real_time/analyzer.py를 이용하여 ROS와 결합하는 과정을 진행함. 기존에 만들어두었던 reciever 노드에서 다시 analyzer로 데이터를 보내는 것과 reciever가 보낸 데이터를 analyzer 코드 안에서 가공하는 노드를 생각했는데, 결합하는 과정에서 여러 오류가 발생함. 현재 오류들을 잡는 과정에 있으며, 수요일 회의 전까지 analyzer 코드를 완성하는 게 목표임.

### 2019-7-23 (화)
1. analyzer 코드 작성
> data_receiver가 보낸 데이터를 analzyer가 받는 것까지는 성공했으나, ctrl+C를 눌러야 callback 함수를 벗어나는 오류와 노드를 완전히 종료하려면 ctrl+z를 눌러야 하는 오류가 있음. 

### 2019-7-24 (수)
1. 회의
> 화요일까지의 analyzer 코드 진행 상황 보고.

2. try_data_analyzer 코드 생성
> 어제까지 진행한 코드를 변경한 [try_data_analyzer](https://github.com/seonghapark/counterUAV/blob/sum2019/ROS_system/try/try_data_analyzer.py) 코드를 만듦. ctrl+C를 눌러야 callback 함수를 벗어나는 오류를 고치기 위해 자료조사하던 중 rospy.Subscriber.unregister() 함수를 찾아서 여러 위치에 넣어봤으나 callback 함수를 벗어나지 못했음. 다른 방법을 더 생각해보아야 할 것 같음.

> try_data_analyzer에서는 callback 함수에 get() 코드를 포함시켜 넘어오는 데이터마다 비트연산을 하도록 수정했음. 코드 수정 중 ifft_handler()에 대한 처리 순서를 고민했었음. get()에서 받아온 데이터에 대한 처리를 한 것을 모두 합쳐서 푸리에 변환을 해야한다고 생각했는데, 원래 코드(2_analyzer.py)를 다시 보니 데이터를 받아올 때마다 푸리에 변환을 하는 것으로 파악하여 ifft_handler()도 get()과 마찬가지로 callback()에서 바로 처리해도 될 것 같음.

### 2019-7-25 (목)
1. [try_data_analyzer](ROS_system/try/try_data_analyzer.py) 코드 완성
> data_receiver에서 보내는 데이터를 받아와서 비트연산(get)과 푸리에 변환(ifft_handler)을 한 후, 다시 publish 하는 코드를 완성함. 어제 생각했던대로 데이터를 받자마자 callback 안에서 get과 ifft_handler 처리를 한 후, publish를 하는 코드로 완성함.

> get과 ifft_handler가 잘 처리되었는지는 시각화를 해보아야 알 수 있을 것 같음. 전송하고, 수신하는 데이터를 출력해보아도 사람이 이해할 수 없는 형태로 출력됨.

> 이전에 막히던 부분인 ctrl+C를 눌러야 이후의 과정이 실행되었던 건 callback() 함수가 계속 돌아가고 있기 때문이었음. callback 안에 get(), ifft_handler를 넣기 전에는 ctrl+C를 눌러 callback을 벗어나야 다음 과정이 실행이 되었던 것인데 완성한 코드에서는 callback() 안에서 다 실행을 하므로 코드 자체를 멈추기 위해서만 ctrl+C를 누르면 됨.

2. test_visualize 코드로 테스트
> try_data_analyzer에서 보낸 데이터를 받는 것을 테스트하기 위해 test_visualize를 작성하여 실행해보았는데, 잘 실행이 되었음. 

> 문제는 파이썬 버전. visualizer에서 사용하는 라이브러리 중 파이썬3에서 사용하는 라이브러리가 있는데, 데이터를 보내는 try_data_analyzer는 파이썬2를 사용함. 데이터를 보내는 건 버전 2로, 받는 건 3으로 테스트 해보았는데 실행이 안 되었음. 그렇다고, try_data_analyzer를 파이썬 3로 실행하면 encoding 문제가 계속 발생함. 버전 문제에 대해서는 더 알아보거나, 생각해보아야 할 것 같음.
