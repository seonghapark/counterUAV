#!/usr/bin/env python3
import rospy
from ros_counteruav.msg import testdata

def callback(msg):
    print('{}'.format(msg.some_int))
    print(len(msg.some_int))
    
def AFCCS():
    #AFCCS_send = rospy.Publisher('AFCCS_send', testdata, queue_size=1)
    rospy.init_node('AFCCS', anonymous=True)
    print('AFCCS ready')
    rospy.Subscriber('MCRC_send', testdata, callback)
    rospy.spin()

if __name__ == '__main__':
    AFCCS()
