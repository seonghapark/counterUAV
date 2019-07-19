#include "ros/ros.h"
#include "ros_counteruav/fakedata.h"

void msgCallback(const ros_counteruav::fakedata::ConstPtr& msg){
	ROS_INFO("recieve msg : %c", msg->data);
}

int main(int argc, char **argv){
	ros::init(argc, argv, "fake_data_subscriber");
	ros::NodeHandle nh;

	ros::Subscriber sub = nh.subscribe("Data", 1000, msgCallback);

	ros::spin();

	return 0;
}
