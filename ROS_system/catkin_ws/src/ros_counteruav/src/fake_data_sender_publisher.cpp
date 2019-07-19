#include "ros/ros.h"
#include "fake_data_sender/FakeData.h"
#include "ros/package.h"
#include <fstream>
#include <iostream>
#include <cstdlib>
#include <string>
#include <sstream>

int main(int argc, char **argv)
{
	int line, i=0, j=0, sz;
	char tstr[4021332];	//raw_data의 최대 파일 크기 입력

	ros::init(argc, argv, "fake_data_sender_publisher");
	ros::NodeHandle nh;

	ros::Publisher sender =   nh.advertise<fake_data_sender::FakeData>("Data", 1000);
	
	ros::Rate loop_rate(1000);

	fake_data_sender::FakeData msg;

	std::ifstream in;

	//c++ binary를 이용한 파일 입출력(참고자료) : https://m.blog.naver.com/PostView.nhn?blogId=infoefficien&logNo=220437327307&proxyReferer=https%3A%2F%2Fwww.google.com%2F
	
	in.open("/home/yeon/catkin_ws/src/fake_data_sender/src/20181009_100023_binary.txt", std::ios::binary);	//절대경로로 경로 읽기(binary 파일 열기)

	/*/////////////////////////////////////////////////////////////////////////////////////////////////////////////
	////////////////////////////ros::package::getPath() 이용한 파일 읽기//////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////////////////////////////////////////////
	std::string s = "/src/20181009_100023_binary.txt";	//getPath 사용할 경우 이용
	in.open((ros::package::getPath("fake_data_sender")+s), std::ios::binary);	//getPath로 경로 읽기(binary 파일 열기)
	ROS_INFO("%s%s",ros::package::getPath("fake_data_sender").c_str(),s.c_str());	//getPath 경로 확인
	*/
	
	ROS_INFO("Publisher START");

	if(in.is_open())	//파일 열기 성공하면
	{
		in.seekg(0, std::ios::end);	//seekg()를 이용하여 파일의 마지막으로 포인터를 옮긴다.
		sz=in.tellg();	//tellg()를 이용하여 파일의 사이즈를 구한다.
		in.seekg(0, std::ios::beg);	//seekg()를 이용하여 다시 파일의 처음으로 포인터를 옮긴다.		
		
		in.read(tstr, sz);	//binary로 파일을 읽을 때는 read함수로 읽는다.		
		
		line = sizeof(tstr)/11724;	// 한 파일의 라인 수 

	}else{
		ROS_INFO("Fail to read file");
	}
	
	while( ros::ok()){
		
		for(; i<line; i++){		//라인 읽기
			for(;j<(i+1)*11724;j++){	//라인 내 한 글자씩 읽기
				msg.data=tstr[j];
				sender.publish(msg);	//바이너리 파일의 한 글자씩 메세지에 담아서 subscriber에게 보내기
			}
			ROS_INFO("%d line complete", i+1);
		}		
		loop_rate.sleep();
		
	}
	
	in.close();

	return 0;
	
}


