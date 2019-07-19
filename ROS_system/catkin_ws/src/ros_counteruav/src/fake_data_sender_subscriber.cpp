#include "ros/ros.h"
#include "fake_data_sender/FakeData.h"

void msgCallback(const fake_data_sender::FakeData::ConstPtr& msg){
	ROS_INFO("recieve msg : %c", msg->data);
}

int main(int argc, char **argv){
	ros::init(argc, argv, "fake_data_subscriber");
	ros::NodeHandle nh;

	ros::Subscriber sub = nh.subscribe("Data", 1000, msgCallback);

	ros::spin();

	return 0;
}
