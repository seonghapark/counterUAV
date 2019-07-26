;; Auto-generated. Do not edit!


(when (boundp 'ros_counteruav::result)
  (if (not (find-package "ROS_COUNTERUAV"))
    (make-package "ROS_COUNTERUAV"))
  (shadow 'result (find-package "ROS_COUNTERUAV")))
(unless (find-package "ROS_COUNTERUAV::RESULT")
  (make-package "ROS_COUNTERUAV::RESULT"))

(in-package "ROS")
;;//! \htmlinclude result.msg.html


(defclass ros_counteruav::result
  :super ros::object
  :slots (_data _time ))

(defmethod ros_counteruav::result
  (:init
   (&key
    ((:data __data) "")
    ((:time __time) "")
    )
   (send-super :init)
   (setq _data (string __data))
   (setq _time (string __time))
   self)
  (:data
   (&optional __data)
   (if __data (setq _data __data)) _data)
  (:time
   (&optional __time)
   (if __time (setq _time __time)) _time)
  (:serialization-length
   ()
   (+
    ;; string _data
    4 (length _data)
    ;; string _time
    4 (length _time)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _data
       (write-long (length _data) s) (princ _data s)
     ;; string _time
       (write-long (length _time) s) (princ _time s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _data
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _data (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _time
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _time (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(setf (get ros_counteruav::result :md5sum-) "07e5952ea6719687121137e7c34f92e3")
(setf (get ros_counteruav::result :datatype-) "ros_counteruav/result")
(setf (get ros_counteruav::result :definition-)
      "string data
string time

")



(provide :ros_counteruav/result "07e5952ea6719687121137e7c34f92e3")


