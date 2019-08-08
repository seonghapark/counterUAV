;; Auto-generated. Do not edit!


(when (boundp 'ros_counteruav::wav)
  (if (not (find-package "ROS_COUNTERUAV"))
    (make-package "ROS_COUNTERUAV"))
  (shadow 'wav (find-package "ROS_COUNTERUAV")))
(unless (find-package "ROS_COUNTERUAV::WAV")
  (make-package "ROS_COUNTERUAV::WAV"))

(in-package "ROS")
;;//! \htmlinclude wav.msg.html


(defclass ros_counteruav::wav
  :super ros::object
  :slots (_wavdata _time ))

(defmethod ros_counteruav::wav
  (:init
   (&key
    ((:wavdata __wavdata) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:time __time) 0)
    )
   (send-super :init)
   (setq _wavdata __wavdata)
   (setq _time (round __time))
   self)
  (:wavdata
   (&optional __wavdata)
   (if __wavdata (setq _wavdata __wavdata)) _wavdata)
  (:time
   (&optional __time)
   (if __time (setq _time __time)) _time)
  (:serialization-length
   ()
   (+
    ;; float32[] _wavdata
    (* 4    (length _wavdata)) 4
    ;; int32 _time
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32[] _wavdata
     (write-long (length _wavdata) s)
     (dotimes (i (length _wavdata))
       (sys::poke (elt _wavdata i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; int32 _time
       (write-long _time s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32[] _wavdata
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _wavdata (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _wavdata i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;; int32 _time
     (setq _time (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get ros_counteruav::wav :md5sum-) "9c745b9bbbbcdca306399d485d1fa8c2")
(setf (get ros_counteruav::wav :datatype-) "ros_counteruav/wav")
(setf (get ros_counteruav::wav :definition-)
      "float32[] wavdata
int32 time
")



(provide :ros_counteruav/wav "9c745b9bbbbcdca306399d485d1fa8c2")


