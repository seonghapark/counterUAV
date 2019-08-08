#!/bin/sh
gnome-terminal -e "roscore"
sleep 5 
gnome-terminal -e "rosrun ros_counteruav RNN.py"
sleep 10 
gnome-terminal -e "rosrun ros_counteruav RNN_stack.py"
sleep 3 
gnome-terminal -e "rosrun ros_counteruav fake_data_sender.py"
sleep 3 
#gnome-terminal -e "rqt_graph"
