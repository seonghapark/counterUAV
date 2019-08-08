#!/usr/bin/env python3
import rospy
from ros_counteruav.msg import testdata

def callback(msg):
    print('{}'.format(msg.some_int))
    print(len(msg.some_int))
    MCRC_send = rospy.Publisher('MCRC_send', testdata, queue_size=1)
    message = testdata()
    message.some_int = msg.some_int
    MCRC_send.publish(message)

def MCRC():
    MCRC_send = rospy.Publisher('MCRC_send', testdata, queue_size=1)
    rospy.init_node('MCRC', anonymous=True)
    print('MCRC ready')
    rospy.Subscriber('radar_send', testdata, callback)
    rospy.spin()

if __name__ == '__main__':
    MCRC()
