#!/usr/bin/env python3
import rospy
from ros_counteruav.msg import testdata

hz = 0.2
time_sec = 5

def radar():
    rospy.init_node('radar', anonymous=True)
    rate = rospy.Rate(hz) # 1hz
    file_name = '/home/project/counterUAV/ROS_system/catkin_ws/src/ros_counteruav/20181009_100023_binary.txt'
    file = open(file_name, "rb")
    read_line = file.readline()
    print('radar ready')
    message = testdata()
    message.some_int = read_line
    i=0
    while not rospy.is_shutdown():
        radar_send = rospy.Publisher('radar_send', testdata, queue_size=1)
        print(len(read_line))
        max = int(len(read_line)//11052)
        print(max)
        if i+time_sec >= max:
            break
        raw = read_line[i*11052:(i+time_sec)*11052]
        print('{} sec send'.format(i))
        #print(type(raw))
        radar_send.publish(raw)
        i += 1
        #i += time_sec
        #i=max
        rate.sleep()

if __name__ == '__main__':
    try:
        radar()
        
    except rospy.ROSInterruptException:
        pass
