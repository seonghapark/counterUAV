#!/usr/bin/env python3
import rospy
from ros_counteruav.msg import testdata

def radar():
    rospy.init_node('radar', anonymous=True)
    rate = rospy.Rate(1) # 1hz
    file_name = '/home/project/counterUAV/ROS_system/catkin_ws/src/ros_counteruav/20181009_100023_binary.txt'
    file = open(file_name, "rb")
    read_line = file.readline()
    print('radar ready')
    message = testdata()
    message.some_int = read_line
    i=0
    while not rospy.is_shutdown():
        radar_send = rospy.Publisher('radar_send', testdata, queue_size=1)
        max = int(len(read_line)//5862)
        if i == max:
            break
        raw = read_line[i*5862:(i+1)*5862]
        print('{} sec send'.format(i))
        print(type(raw))
        radar_send.publish(raw)
        i += 1
        #i=max
        rate.sleep()

if __name__ == '__main__':
    try:
        radar()
        
    except rospy.ROSInterruptException:
        pass