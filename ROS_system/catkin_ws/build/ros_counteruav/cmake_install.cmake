# Install script for directory: /home/project/counterUAV/ROS_system/catkin_ws/src/ros_counteruav

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/project/counterUAV/ROS_system/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  include("/home/project/counterUAV/ROS_system/catkin_ws/build/ros_counteruav/catkin_generated/safe_execute_install.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ros_counteruav/msg" TYPE FILE FILES
    "/home/project/counterUAV/ROS_system/catkin_ws/src/ros_counteruav/msg/fakedata.msg"
    "/home/project/counterUAV/ROS_system/catkin_ws/src/ros_counteruav/msg/result.msg"
    "/home/project/counterUAV/ROS_system/catkin_ws/src/ros_counteruav/msg/wav.msg"
    "/home/project/counterUAV/ROS_system/catkin_ws/src/ros_counteruav/msg/objectinfo.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ros_counteruav/cmake" TYPE FILE FILES "/home/project/counterUAV/ROS_system/catkin_ws/build/ros_counteruav/catkin_generated/installspace/ros_counteruav-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/project/counterUAV/ROS_system/catkin_ws/devel/include/ros_counteruav")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/project/counterUAV/ROS_system/catkin_ws/devel/share/roseus/ros/ros_counteruav")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/project/counterUAV/ROS_system/catkin_ws/devel/share/common-lisp/ros/ros_counteruav")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/project/counterUAV/ROS_system/catkin_ws/devel/share/gennodejs/ros/ros_counteruav")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/project/counterUAV/ROS_system/catkin_ws/devel/lib/python3/dist-packages/ros_counteruav")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/project/counterUAV/ROS_system/catkin_ws/devel/lib/python3/dist-packages/ros_counteruav" REGEX "/\\_\\_init\\_\\_\\.py$" EXCLUDE REGEX "/\\_\\_init\\_\\_\\.pyc$" EXCLUDE)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/project/counterUAV/ROS_system/catkin_ws/devel/lib/python3/dist-packages/ros_counteruav" FILES_MATCHING REGEX "/home/project/counterUAV/ROS_system/catkin_ws/devel/lib/python3/dist-packages/ros_counteruav/.+/__init__.pyc?$")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/project/counterUAV/ROS_system/catkin_ws/build/ros_counteruav/catkin_generated/installspace/ros_counteruav.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ros_counteruav/cmake" TYPE FILE FILES "/home/project/counterUAV/ROS_system/catkin_ws/build/ros_counteruav/catkin_generated/installspace/ros_counteruav-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ros_counteruav/cmake" TYPE FILE FILES
    "/home/project/counterUAV/ROS_system/catkin_ws/build/ros_counteruav/catkin_generated/installspace/ros_counteruavConfig.cmake"
    "/home/project/counterUAV/ROS_system/catkin_ws/build/ros_counteruav/catkin_generated/installspace/ros_counteruavConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ros_counteruav" TYPE FILE FILES "/home/project/counterUAV/ROS_system/catkin_ws/src/ros_counteruav/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/project/counterUAV/ROS_system/catkin_ws/build/ros_counteruav/catkin_generated/installspace/ros_counteruav.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ros_counteruav/cmake" TYPE FILE FILES "/home/project/counterUAV/ROS_system/catkin_ws/build/ros_counteruav/catkin_generated/installspace/ros_counteruav-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ros_counteruav/cmake" TYPE FILE FILES
    "/home/project/counterUAV/ROS_system/catkin_ws/build/ros_counteruav/catkin_generated/installspace/ros_counteruavConfig.cmake"
    "/home/project/counterUAV/ROS_system/catkin_ws/build/ros_counteruav/catkin_generated/installspace/ros_counteruavConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ros_counteruav" TYPE FILE FILES "/home/project/counterUAV/ROS_system/catkin_ws/src/ros_counteruav/package.xml")
endif()

