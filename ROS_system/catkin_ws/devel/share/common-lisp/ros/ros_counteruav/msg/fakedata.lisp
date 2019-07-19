; Auto-generated. Do not edit!


(cl:in-package ros_counteruav-msg)


;//! \htmlinclude fakedata.msg.html

(cl:defclass <fakedata> (roslisp-msg-protocol:ros-message)
  ((data
    :reader data
    :initarg :data
    :type cl:integer
    :initform 0))
)

(cl:defclass fakedata (<fakedata>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <fakedata>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'fakedata)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_counteruav-msg:<fakedata> is deprecated: use ros_counteruav-msg:fakedata instead.")))

(cl:ensure-generic-function 'data-val :lambda-list '(m))
(cl:defmethod data-val ((m <fakedata>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_counteruav-msg:data-val is deprecated.  Use ros_counteruav-msg:data instead.")
  (data m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <fakedata>) ostream)
  "Serializes a message object of type '<fakedata>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'data)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <fakedata>) istream)
  "Deserializes a message object of type '<fakedata>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'data)) (cl:read-byte istream))
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
  "ad736a2e8818154c487bb80fe42ce43b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'fakedata)))
  "Returns md5sum for a message object of type 'fakedata"
  "ad736a2e8818154c487bb80fe42ce43b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<fakedata>)))
  "Returns full string definition for message of type '<fakedata>"
  (cl:format cl:nil "byte data~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'fakedata)))
  "Returns full string definition for message of type 'fakedata"
  (cl:format cl:nil "byte data~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <fakedata>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <fakedata>))
  "Converts a ROS message object to a list"
  (cl:list 'fakedata
    (cl:cons ':data (data msg))
))
