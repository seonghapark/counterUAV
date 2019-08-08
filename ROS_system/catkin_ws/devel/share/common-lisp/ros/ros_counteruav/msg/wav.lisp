; Auto-generated. Do not edit!


(cl:in-package ros_counteruav-msg)


;//! \htmlinclude wav.msg.html

(cl:defclass <wav> (roslisp-msg-protocol:ros-message)
  ((wavdata
    :reader wavdata
    :initarg :wavdata
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (time
    :reader time
    :initarg :time
    :type cl:integer
    :initform 0))
)

(cl:defclass wav (<wav>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <wav>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'wav)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_counteruav-msg:<wav> is deprecated: use ros_counteruav-msg:wav instead.")))

(cl:ensure-generic-function 'wavdata-val :lambda-list '(m))
(cl:defmethod wavdata-val ((m <wav>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_counteruav-msg:wavdata-val is deprecated.  Use ros_counteruav-msg:wavdata instead.")
  (wavdata m))

(cl:ensure-generic-function 'time-val :lambda-list '(m))
(cl:defmethod time-val ((m <wav>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_counteruav-msg:time-val is deprecated.  Use ros_counteruav-msg:time instead.")
  (time m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <wav>) ostream)
  "Serializes a message object of type '<wav>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'wavdata))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'wavdata))
  (cl:let* ((signed (cl:slot-value msg 'time)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <wav>) istream)
  "Deserializes a message object of type '<wav>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'wavdata) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'wavdata)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits))))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'time) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<wav>)))
  "Returns string type for a message object of type '<wav>"
  "ros_counteruav/wav")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'wav)))
  "Returns string type for a message object of type 'wav"
  "ros_counteruav/wav")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<wav>)))
  "Returns md5sum for a message object of type '<wav>"
  "9c745b9bbbbcdca306399d485d1fa8c2")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'wav)))
  "Returns md5sum for a message object of type 'wav"
  "9c745b9bbbbcdca306399d485d1fa8c2")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<wav>)))
  "Returns full string definition for message of type '<wav>"
  (cl:format cl:nil "float32[] wavdata~%int32 time~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'wav)))
  "Returns full string definition for message of type 'wav"
  (cl:format cl:nil "float32[] wavdata~%int32 time~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <wav>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'wavdata) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <wav>))
  "Converts a ROS message object to a list"
  (cl:list 'wav
    (cl:cons ':wavdata (wavdata msg))
    (cl:cons ':time (time msg))
))
