#!/usr/bin/env python3
import rospy
from ros_counteruav.msg import objectinfo

def callback(msg):
    print('stay')
    print('{}'.format(msg.who))

def USER():
    rospy.init_node('USER', anonymous=True)
    print('USER ready')
    rospy.Subscriber('RAWS_send', objectinfo, callback)
    rospy.spin()

if __name__ == '__main__':
    USER()
