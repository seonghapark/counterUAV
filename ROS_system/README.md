ROS_system
=======
## counter UAV ROS system 입니다

### 반드시 우분투 기준 
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

