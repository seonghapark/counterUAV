#!/bin/sh
gnome-terminal -e "roscore"
sleep 5 
gnome-terminal -e "rosrun ros_counteruav visualizer.py"
sleep 5
gnome-terminal -e "rosrun ros_counteruav data_analyzer.py"
sleep 5 
gnome-terminal -e "rosrun ros_counteruav data_receiver.py"
sleep 5 
gnome-terminal -e "rosrun ros_counteruav RNN.py"
sleep 10 
gnome-terminal -e "rosrun ros_counteruav RNN_stack.py"
sleep 3 
gnome-terminal -e "rosrun ros_counteruav fake_data_sender.py /home/project/counterUAV/raw_data/20181009_100023_binary.txt"
sleep 3 
gnome-terminal -e "rqt_graph"
#gnome-terminal -e "rqt_graph"
