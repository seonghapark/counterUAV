ROS_system
=======
## How to start counterUAV

### Download and set permission
```
$ sudo mkdir -p /home/project
$ sudo chmod 777 /home/project
$ cd /home/project/
```

전체 프로젝트를 다운받으려면

```
$ git clone https://github.com/seonghapark/counterUAV.git
$ git checkout fall2019
```

이 브랜치만 다운받으려면
```
$ git clone -b fall2019 --single-branch https://github.com/seonghapark/counterUAV.git
```


###  install in Ubuntu
```
$ wget https://raw.githubusercontent.com/orocapangyo/meetup/master/190830/install_ros_melodic.sh && chmod 755 ./install_ros_melodic.sh && bash ./install_ros_melodic.sh
```

### NTP(Network Time Protocol) 설정
```
$ sudo apt-get install -y chrony ntpdate
$ sudo ntpdate -q ntp.ubuntu.com
```

### 소스 리스트 추가 
```
$ sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
```

### 키 설정
```
$ sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
```

### 패키지 인덱스 업데이트
```
$ sudo apt-get update
```

### ROS Melodic 설치
```
$ sudo apt install ros-melodic-desktop-full

# 설치 확인
$ apt search ros-melodic
```

### Initialize rosdep
```
$ sudo rosdep init
$ rosdep update
```

### rosinstall 설치
```
$ sudo apt-get install python-rosinstall
```

### bashrc 설정
`vi ~/.bashrc`에 들어가서

```
#ROS
alias eb='nano ~/.bashrc'
alias sb='source ~/.bashrc'
alias cw='cd /home/project/counterUAV/ROS_system/catkin_ws'
alias cs='cd /home/project/counterUAV/ROS_system/catkin_ws/src'
alias cm='cd /home/project/counterUAV/ROS_system/catkin_ws && catkin_make'
source /opt/ros/melodic/setup.bash
source /home/project/counterUAV/ROS_system/catkin_ws/devel/setup.bash
export ROS_PACKAGE_PATH=/home/project/counterUAV/ROS_system/catkin_ws/src/:/opt/ros/melodic/share
export ROS_MASTER_URI=http://localhost:11311
export ROS_HOSTNAME=localhost
```
입력

```
$ source ~/.bashrc
```

### 파이썬 패키지 설치
```
$ sudo apt install python-rosinstall python-rosinstall-generator python-wstool build-essential
$ pip3 install scipy librosa tensorflow flask pika rospkg catkin_pkg matplotlib
```


### ros make

catkin_ws 폴더에 들어가서

```
$ pip3 install empy
$ catkin_make
```

### ros 실행 >> 오류날경우 bashrc 다시 설정

```
$ roscore
```

새로운 터미널을 연 뒤
`/home/project/counterUAV/ROS_system/catkin_ws` 에서
```
$ rosrun ros_counteruav scripts/start.sh
```




---------

## counter UAV ROS system 입니다

### 반드시 우분투 기준 


### 
byte array를 쓰고 싶어요<br>
1. #!/usr/bin/env python3<br>
2. testdata.msg 생성 후 uint8[] some_int // 파이썬3에서는 uint8이 byte고 uint8[]이 bytes이다.
3. from ros_counteruav.msg import testdata  // <br> [ros msg형태](http://wiki.ros.org/msg), [ros array 사용하기](https://answers.ros.org/question/9471/how-to-recieve-an-array-over-publisher-and-subscriber-python/)<br>
4. radar_send = rospy.Publisher('radar_send', testdata, queue_size=1) // 퍼블리셔<br>
5. message.some_int = read_line // 메시지에 데이터 저장 testdata.msg 안에 uint8[] <변수명> 요거 적어주면 된다.<br>
6. rospy.Subscriber('radar_send', testdata, callback) // subscriber <br>
링크를 클릭해 보심 더 빠릅니다.
