; Auto-generated. Do not edit!


(cl:in-package ros_counteruav-msg)


;//! \htmlinclude result.msg.html

(cl:defclass <result> (roslisp-msg-protocol:ros-message)
  ((data
    :reader data
    :initarg :data
    :type cl:string
    :initform "")
   (time
    :reader time
    :initarg :time
    :type cl:string
    :initform ""))
)

(cl:defclass result (<result>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <result>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'result)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_counteruav-msg:<result> is deprecated: use ros_counteruav-msg:result instead.")))

(cl:ensure-generic-function 'data-val :lambda-list '(m))
(cl:defmethod data-val ((m <result>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_counteruav-msg:data-val is deprecated.  Use ros_counteruav-msg:data instead.")
  (data m))

(cl:ensure-generic-function 'time-val :lambda-list '(m))
(cl:defmethod time-val ((m <result>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_counteruav-msg:time-val is deprecated.  Use ros_counteruav-msg:time instead.")
  (time m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <result>) ostream)
  "Serializes a message object of type '<result>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'data))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'data))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'time))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'time))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <result>) istream)
  "Deserializes a message object of type '<result>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'data) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'data) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'time) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'time) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<result>)))
  "Returns string type for a message object of type '<result>"
  "ros_counteruav/result")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'result)))
  "Returns string type for a message object of type 'result"
  "ros_counteruav/result")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<result>)))
  "Returns md5sum for a message object of type '<result>"
  "07e5952ea6719687121137e7c34f92e3")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'result)))
  "Returns md5sum for a message object of type 'result"
  "07e5952ea6719687121137e7c34f92e3")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<result>)))
  "Returns full string definition for message of type '<result>"
  (cl:format cl:nil "string data~%string time~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'result)))
  "Returns full string definition for message of type 'result"
  (cl:format cl:nil "string data~%string time~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <result>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'data))
     4 (cl:length (cl:slot-value msg 'time))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <result>))
  "Converts a ROS message object to a list"
  (cl:list 'result
    (cl:cons ':data (data msg))
    (cl:cons ':time (time msg))
))
