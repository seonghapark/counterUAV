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
  :slots (_data ))

(defmethod ros_counteruav::fakedata
  (:init
   (&key
    ((:data __data) 0)
    )
   (send-super :init)
   (setq _data (round __data))
   self)
  (:data
   (&optional __data)
   (if __data (setq _data __data)) _data)
  (:serialization-length
   ()
   (+
    ;; byte _data
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; byte _data
       (write-byte _data s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; byte _data
     (setq _data (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _data 127) (setq _data (- _data 256)))
   ;;
   self)
  )

(setf (get ros_counteruav::fakedata :md5sum-) "ad736a2e8818154c487bb80fe42ce43b")
(setf (get ros_counteruav::fakedata :datatype-) "ros_counteruav/fakedata")
(setf (get ros_counteruav::fakedata :definition-)
      "byte data
")



(provide :ros_counteruav/fakedata "ad736a2e8818154c487bb80fe42ce43b")


