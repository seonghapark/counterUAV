// Generated by gencpp from file ros_counteruav/objectinfo.msg
// DO NOT EDIT!


#ifndef ROS_COUNTERUAV_MESSAGE_OBJECTINFO_H
#define ROS_COUNTERUAV_MESSAGE_OBJECTINFO_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace ros_counteruav
{
template <class ContainerAllocator>
struct objectinfo_
{
  typedef objectinfo_<ContainerAllocator> Type;

  objectinfo_()
    : who()
    , time(0)  {
    }
  objectinfo_(const ContainerAllocator& _alloc)
    : who(_alloc)
    , time(0)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _who_type;
  _who_type who;

   typedef int32_t _time_type;
  _time_type time;





  typedef boost::shared_ptr< ::ros_counteruav::objectinfo_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::ros_counteruav::objectinfo_<ContainerAllocator> const> ConstPtr;

}; // struct objectinfo_

typedef ::ros_counteruav::objectinfo_<std::allocator<void> > objectinfo;

typedef boost::shared_ptr< ::ros_counteruav::objectinfo > objectinfoPtr;
typedef boost::shared_ptr< ::ros_counteruav::objectinfo const> objectinfoConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::ros_counteruav::objectinfo_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::ros_counteruav::objectinfo_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace ros_counteruav

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsMessage': True, 'IsFixedSize': False, 'HasHeader': False}
// {'ros_counteruav': ['/home/project/counterUAV/ROS_system/catkin_ws/src/ros_counteruav/msg'], 'std_msgs': ['/opt/ros/melodic/share/std_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsMessage< ::ros_counteruav::objectinfo_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ros_counteruav::objectinfo_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ros_counteruav::objectinfo_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ros_counteruav::objectinfo_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ros_counteruav::objectinfo_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ros_counteruav::objectinfo_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::ros_counteruav::objectinfo_<ContainerAllocator> >
{
  static const char* value()
  {
    return "59a9b469fbe19b4315bbcb0d3d4775aa";
  }

  static const char* value(const ::ros_counteruav::objectinfo_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x59a9b469fbe19b43ULL;
  static const uint64_t static_value2 = 0x15bbcb0d3d4775aaULL;
};

template<class ContainerAllocator>
struct DataType< ::ros_counteruav::objectinfo_<ContainerAllocator> >
{
  static const char* value()
  {
    return "ros_counteruav/objectinfo";
  }

  static const char* value(const ::ros_counteruav::objectinfo_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::ros_counteruav::objectinfo_<ContainerAllocator> >
{
  static const char* value()
  {
    return "string who\n"
"int32 time\n"
;
  }

  static const char* value(const ::ros_counteruav::objectinfo_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::ros_counteruav::objectinfo_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.who);
      stream.next(m.time);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct objectinfo_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::ros_counteruav::objectinfo_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::ros_counteruav::objectinfo_<ContainerAllocator>& v)
  {
    s << indent << "who: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.who);
    s << indent << "time: ";
    Printer<int32_t>::stream(s, indent + "  ", v.time);
  }
};

} // namespace message_operations
} // namespace ros

#endif // ROS_COUNTERUAV_MESSAGE_OBJECTINFO_H
