; Auto-generated. Do not edit!


(cl:in-package ros_counteruav-msg)


;//! \htmlinclude fakedata.msg.html

(cl:defclass <fakedata> (roslisp-msg-protocol:ros-message)
  ((num
    :reader num
    :initarg :num
    :type cl:integer
    :initform 0))
)

(cl:defclass fakedata (<fakedata>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <fakedata>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'fakedata)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_counteruav-msg:<fakedata> is deprecated: use ros_counteruav-msg:fakedata instead.")))

(cl:ensure-generic-function 'num-val :lambda-list '(m))
(cl:defmethod num-val ((m <fakedata>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_counteruav-msg:num-val is deprecated.  Use ros_counteruav-msg:num instead.")
  (num m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <fakedata>) ostream)
  "Serializes a message object of type '<fakedata>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'num)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <fakedata>) istream)
  "Deserializes a message object of type '<fakedata>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'num)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<fakedata>)))
  "Returns string type for a message object of type '<fakedata>"
  "ros_counteruav/fakedata")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'fakedata)))
  "Returns string type for a message object of type 'fakedata"
  "ros_counteruav/fakedata")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<fakedata>)))
  "Returns md5sum for a message object of type '<fakedata>"
  "a42f91c6165312a676067eda99ad61b7")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'fakedata)))
  "Returns md5sum for a message object of type 'fakedata"
  "a42f91c6165312a676067eda99ad61b7")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<fakedata>)))
  "Returns full string definition for message of type '<fakedata>"
  (cl:format cl:nil "byte num~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'fakedata)))
  "Returns full string definition for message of type 'fakedata"
  (cl:format cl:nil "byte num~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <fakedata>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <fakedata>))
  "Converts a ROS message object to a list"
  (cl:list 'fakedata
    (cl:cons ':num (num msg))
))
