#! /usr/bin/env python3
from flask import Flask
import rospy
from ros_counteruav.msg import fakedata
from threading import Thread
#from std_msgs.msg import String

app = Flask(__name__)


@app.route('/listener')
def listener():
    #print('listener START')
    #rospy.init_node('visualizer_receiver', anonymous=True)
    rospy.Subscriber('analyzed_data', fakedata, callback)
    #print('BEFORE spin')
    rospy.spin()
    #print('AFTER spin')
    
def callback(data):
    #print('START callback')
    #print(data.data)
    #print('FINISH callback')
    return "<h1>hello<h1>"




@app.route("/hello/")
def hello():                           
    return "<h1>Hello World!</h1>"


if __name__=='__main__':
    rospy.init_node('visualizer_receiver', anonymous=True)
    app.run(host="localhost",port='8080')
