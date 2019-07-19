ROS_system
=======
## counter UAV ROS system 입니다

### 반드시 우분투 기준 
> cd /home/project/ 
> git clone https://github.com/seonghapark/counterUAV.git
> git checkout sum2019

# bashrc 설정
>alias eb='nano ~/.bashrc'
alias sb='source ~/.bashrc'
alias cw='cd /home/project/counterUAV/ROS_system/catkin_ws'
alias cs='cd /home/project/counterUAV/ROS_system/catkin_ws/src'
alias cm='cd /home/project/counterUAV/ROS_system/catkin_ws && catkin_make'
source /opt/ros/melodic/setup.bash
source /home/project/counterUAV/ROS_system/catkin_ws/devel/setup.bash
export ROS_PACKAGE_PATH=/home/project/counterUAV/ROS_system/catkin_ws/src/:/opt/ros/melodic/share
export ROS_MASTER_URI=http://localhost:11311
export ROS_HOSTNAME=localhost

