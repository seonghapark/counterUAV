;; Auto-generated. Do not edit!


(when (boundp 'ros_counteruav::objectinfo)
  (if (not (find-package "ROS_COUNTERUAV"))
    (make-package "ROS_COUNTERUAV"))
  (shadow 'objectinfo (find-package "ROS_COUNTERUAV")))
(unless (find-package "ROS_COUNTERUAV::OBJECTINFO")
  (make-package "ROS_COUNTERUAV::OBJECTINFO"))

(in-package "ROS")
;;//! \htmlinclude objectinfo.msg.html


(defclass ros_counteruav::objectinfo
  :super ros::object
  :slots (_who _time ))

(defmethod ros_counteruav::objectinfo
  (:init
   (&key
    ((:who __who) "")
    ((:time __time) 0)
    )
   (send-super :init)
   (setq _who (string __who))
   (setq _time (round __time))
   self)
  (:who
   (&optional __who)
   (if __who (setq _who __who)) _who)
  (:time
   (&optional __time)
   (if __time (setq _time __time)) _time)
  (:serialization-length
   ()
   (+
    ;; string _who
    4 (length _who)
    ;; int32 _time
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _who
       (write-long (length _who) s) (princ _who s)
     ;; int32 _time
       (write-long _time s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _who
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _who (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; int32 _time
     (setq _time (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get ros_counteruav::objectinfo :md5sum-) "59a9b469fbe19b4315bbcb0d3d4775aa")
(setf (get ros_counteruav::objectinfo :datatype-) "ros_counteruav/objectinfo")
(setf (get ros_counteruav::objectinfo :definition-)
      "string who
int32 time
")



(provide :ros_counteruav/objectinfo "59a9b469fbe19b4315bbcb0d3d4775aa")


