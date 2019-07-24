ROS_system
=======
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
>sudo apt-get install python3-pip python3-yaml<br>
>pip3 install rospkg catkin_pkg<br>
>sudo apt-get install python-catkin-tools python3-dev python3-numpy<br>
>catkin config -DPYTHON_EXECUTABLE=/usr/bin/python3 -DPYTHON_INCLUDE_DIR=/usr/include/python3.6m -DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.6m.so
>catkin config --install
