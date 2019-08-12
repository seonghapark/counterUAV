#!/usr/bin/env python3

# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic
import sys
import os
import pika
import time
import rospy
#from std_msgs.msg import String
from ros_counteruav.msg import fakedata




def talker():
    #pub = rospy.Publisher('chatter', String, queue_size=10)
    pub = rospy.Publisher('chatter', fakedata, queue_size=10)
    rospy.init_node('fake_data_sender', anonymous=True)
    rate = rospy.Rate(0.8) # 10hz
    # read file
    #pwd = os.getcwd() # current working folder
    #wd = '/home/project/counterUAV/raw_data/'
    #file_name = pwd+ '/' +sys.argv[1]
    #file_name = '/home/project/counterUAV/raw_data/20181114_135427_binary.txt'
    file_name = '/home/project/counterUAV/ROS_system/catkin_ws/src/ros_counteruav/raw_data/'
    file_name = sys.argv[1]
    message = fakedata()
    raw = fakedata()
    file = open(file_name, "rb")
    
    #read_line = file.readline()
    #message.data = file.read()
    #data = bytearray()
    #data = file.read()
    data = file.read()  
    
    max = 0
    i = 0
    j = 0
    max = int(len(data)//(5862*2))
    try:
        # divide input
        while not rospy.is_shutdown():             
            #max = int(len(message.data)//11025)
            
            if i+j <= max : 
                i = i+1 
            else :
                break
            raw.data = data[i*(5862*2):(i+1)*(5862*2)+1]
            if i == 256 :
                j = i + j
                i = 0
            raw.num = i
            #rabbitmq.publish(raw)
            rospy.loginfo("max"+str(max)+" time"+str(i+j)+":"+str(rospy.get_time()))
            pub.publish(raw)
            #pub.publish(raw.data)
            
            rate.sleep()

    except (KeyboardInterrupt, Exception) as ex:
        print(ex)
    finally:
        print('Close all')
        #rabbitmq.connection.close()
        file.close()



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
