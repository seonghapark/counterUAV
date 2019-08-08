; Auto-generated. Do not edit!


(cl:in-package ros_counteruav-msg)


;//! \htmlinclude objectinfo.msg.html

(cl:defclass <objectinfo> (roslisp-msg-protocol:ros-message)
  ((who
    :reader who
    :initarg :who
    :type cl:string
    :initform "")
   (time
    :reader time
    :initarg :time
    :type cl:integer
    :initform 0))
)

(cl:defclass objectinfo (<objectinfo>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <objectinfo>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'objectinfo)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_counteruav-msg:<objectinfo> is deprecated: use ros_counteruav-msg:objectinfo instead.")))

(cl:ensure-generic-function 'who-val :lambda-list '(m))
(cl:defmethod who-val ((m <objectinfo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_counteruav-msg:who-val is deprecated.  Use ros_counteruav-msg:who instead.")
  (who m))

(cl:ensure-generic-function 'time-val :lambda-list '(m))
(cl:defmethod time-val ((m <objectinfo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_counteruav-msg:time-val is deprecated.  Use ros_counteruav-msg:time instead.")
  (time m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <objectinfo>) ostream)
  "Serializes a message object of type '<objectinfo>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'who))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'who))
  (cl:let* ((signed (cl:slot-value msg 'time)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <objectinfo>) istream)
  "Deserializes a message object of type '<objectinfo>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'who) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'who) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'time) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<objectinfo>)))
  "Returns string type for a message object of type '<objectinfo>"
  "ros_counteruav/objectinfo")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'objectinfo)))
  "Returns string type for a message object of type 'objectinfo"
  "ros_counteruav/objectinfo")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<objectinfo>)))
  "Returns md5sum for a message object of type '<objectinfo>"
  "59a9b469fbe19b4315bbcb0d3d4775aa")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'objectinfo)))
  "Returns md5sum for a message object of type 'objectinfo"
  "59a9b469fbe19b4315bbcb0d3d4775aa")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<objectinfo>)))
  "Returns full string definition for message of type '<objectinfo>"
  (cl:format cl:nil "string who~%int32 time~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'objectinfo)))
  "Returns full string definition for message of type 'objectinfo"
  (cl:format cl:nil "string who~%int32 time~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <objectinfo>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'who))
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <objectinfo>))
  "Converts a ROS message object to a list"
  (cl:list 'objectinfo
    (cl:cons ':who (who msg))
    (cl:cons ':time (time msg))
))
