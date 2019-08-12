#! /usr/bin/env python3



import rospy
from ros_counteruav.msg import fakedata
#from std_msgs.msg import String

def callback(data):
    #print('{}'.format(data.data))
    
    #Re_send
    repub = rospy.Publisher('msg_for_analyzer', fakedata, queue_size=1)
    #re_rate = rospy.Rate(1)
    msg = fakedata()
    msg.data = data.data
    msg.num = data.num 
    repub.publish(msg)
    #rospy.loginfo(str(msg.num))
    #re_rate.sleep()

def listener():


    rospy.init_node('data_receiver', anonymous=True)

    rospy.Subscriber('chatter', fakedata, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()
