execute_process(COMMAND "/home/jhjeong/project/counterUAV/ROS_system/catkin_ws/build/ros_counteruav/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/jhjeong/project/counterUAV/ROS_system/catkin_ws/build/ros_counteruav/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
