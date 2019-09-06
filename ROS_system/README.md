ROS_system
=======
## How to install ROS

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
$ sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
```

### 패키지 인덱스 업데이트
```
$ sudo apt-get update && sudo apt-get upgrade -y
```

### ROS Kinetic Kame 설치
```
$ sudo apt-get install ros-kinetic-desktop-full
$ rosdep update
```

### rosinstall 설치
```
$ sudo apt-get install python-rosinstall
```

### bashrc 설정
```
alias eb='nano ~/.bashrc'
alias sb='source ~/.bashrc'
alias cw='cd /home/project/counterUAV/ROS_system/catkin_ws'
alias cs='cd /home/project/counterUAV/ROS_system/catkin_ws/src'
alias cm='cd /home/project/counterUAV/ROS_system/catkin_ws && catkin_make'
source /opt/ros/melodic/setup.bash
source ~/catkin_ws/devel/setup.bash
source /home/project/counterUAV/ROS_system/catkin_ws/devel/setup.bash
export ROS_PACKAGE_PATH=/home/project/counterUAV/ROS_system/catkin_ws/src/:/opt/ros/melodic/share
export ROS_MASTER_URI=http://localhost:11311
export ROS_HOSTNAME=localhost
```

### 패키지 설치
```
$ pip3 install scipy
```


### ros make

catkin_ws 폴더에 들어가서

```
$ pip3 install empy
$ catkin_make
```

### ros 실행

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
> sudo mkdir -p /home/project <br>
> sudo chmod 777 /home/project <br>
> cd /home/project/ <br>

> git clone https://github.com/seonghapark/counterUAV.git<br>
> git checkout sum2019<br>

# bashrc 설정
>alias eb='nano ~/.bashrc' <br>
alias sb='source ~/.bashrc'<br>
alias cw='cd /home/project/counterUAV/ROS_system/catkin_ws'<br>
alias cs='cd /home/project/counterUAV/ROS_system/catkin_ws/src'<br>
alias cm='cd /home/project/counterUAV/ROS_system/catkin_ws && catkin_make'<br>
source /opt/ros/melodic/setup.bash<br>
source /home/project/counterUAV/ROS_system/catkin_ws/devel/setup.bash<br>
export ROS_PACKAGE_PATH=/home/project/counterUAV/ROS_system/catkin_ws/src/:/opt/ros/melodic/share<br>
export ROS_MASTER_URI=http://localhost:11311<br>
export ROS_HOSTNAME=localhost<br>

### python3 적용(불완전)
```
sudo apt-get install python3-pip python3-yaml
pip3 install rospkg catkin_pkg
pip3 install pika
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu `lsb_release -sc` main" > /etc/apt/sources.list.d/ros-latest.list'
wget http://packages.ros.org/ros.key -O - | sudo apt-key add -
sudo apt-get update
sudo apt-get install python-catkin-tools
sudo apt-get install python-catkin-tools python3-dev python3-numpy
catkin config -DPYTHON_EXECUTABLE=/usr/bin/python3 -DPYTHON_INCLUDE_DIR=/usr/include/python3.6m -DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.6m.so
catkin config --install
```

#### .py 파일 첫줄에 
`#!/usr/bin/env python3`
입력

### 
byte array를 쓰고 싶어요<br>
1. #!/usr/bin/env python3<br>
2. testdata.msg 생성 후 uint8[] some_int // 파이썬3에서는 uint8이 byte고 uint8[]이 bytes이다.
3. from ros_counteruav.msg import testdata  // <br> [ros msg형태](http://wiki.ros.org/msg), [ros array 사용하기](https://answers.ros.org/question/9471/how-to-recieve-an-array-over-publisher-and-subscriber-python/)<br>
4. radar_send = rospy.Publisher('radar_send', testdata, queue_size=1) // 퍼블리셔<br>
5. message.some_int = read_line // 메시지에 데이터 저장 testdata.msg 안에 uint8[] <변수명> 요거 적어주면 된다.<br>
6. rospy.Subscriber('radar_send', testdata, callback) // subscriber <br>
링크를 클릭해 보심 더 빠릅니다.


# 최종 실행 코드 경로
>counterUAV/ROS_system/catkin_ws/src/ros_counteruav/scripts/

>위의 경로의 readme에 코드 설명
