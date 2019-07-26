#!/bin/sh
gnome-terminal -e "roscore"
sleep 5 
gnome-terminal -e "rosrun ros_counteruav RAWS.py"
sleep 10 
gnome-terminal -e "rosrun ros_counteruav AFCCS.py"
sleep 3 
gnome-terminal -e "rosrun ros_counteruav MCRC.py"
sleep 3 
gnome-terminal -e "rosrun ros_counteruav radar.py"
gnome-terminal -e "rqt_graph"
#sleep 7
#display -resize "150%" ez.jpeg
