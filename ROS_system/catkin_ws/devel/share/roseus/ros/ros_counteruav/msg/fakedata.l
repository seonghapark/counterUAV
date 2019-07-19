;; Auto-generated. Do not edit!


(when (boundp 'ros_counteruav::fakedata)
  (if (not (find-package "ROS_COUNTERUAV"))
    (make-package "ROS_COUNTERUAV"))
  (shadow 'fakedata (find-package "ROS_COUNTERUAV")))
(unless (find-package "ROS_COUNTERUAV::FAKEDATA")
  (make-package "ROS_COUNTERUAV::FAKEDATA"))

(in-package "ROS")
;;//! \htmlinclude fakedata.msg.html


(defclass ros_counteruav::fakedata
  :super ros::object
  :slots (_num ))

(defmethod ros_counteruav::fakedata
  (:init
   (&key
    ((:num __num) 0)
    )
   (send-super :init)
   (setq _num (round __num))
   self)
  (:num
   (&optional __num)
   (if __num (setq _num __num)) _num)
  (:serialization-length
   ()
   (+
    ;; byte _num
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; byte _num
       (write-byte _num s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; byte _num
     (setq _num (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _num 127) (setq _num (- _num 256)))
   ;;
   self)
  )

(setf (get ros_counteruav::fakedata :md5sum-) "a42f91c6165312a676067eda99ad61b7")
(setf (get ros_counteruav::fakedata :datatype-) "ros_counteruav/fakedata")
(setf (get ros_counteruav::fakedata :definition-)
      "byte num
")



(provide :ros_counteruav/fakedata "a42f91c6165312a676067eda99ad61b7")


