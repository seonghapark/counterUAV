#! /usr/bin/env python3

import rospy
from ros_counteruav.msg import fakedata
#from std_msgs.msg import String

def callback(data):
    print('START callback')
    print(data.data)
    print('FINISH callback')

def listener():
    print('listener START')
    rospy.init_node('visualizer_receiver', anonymous=True)
    rospy.Subscriber('analyzed_data', fakedata, callback)
    print('BEFORE spin')
    rospy.spin()
    print('AFTER spin')

if __name__=='__main__':
    listener()
