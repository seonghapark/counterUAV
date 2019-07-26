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
    ((:data __data) (make-array 0 :initial-element 0 :element-type :char))
    )
   (send-super :init)
   (setq _data __data)
   self)
  (:data
   (&optional __data)
   (if __data (setq _data __data)) _data)
  (:serialization-length
   ()
   (+
    ;; uint8[] _data
    (* 1    (length _data)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8[] _data
     (write-long (length _data) s)
     (princ _data s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8[] _data
   (let ((n (sys::peek buf ptr- :integer))) (incf ptr- 4)
     (setq _data (make-array n :element-type :char))
     (replace _data buf :start2 ptr-) (incf ptr- n))
   ;;
   self)
  )

(setf (get ros_counteruav::fakedata :md5sum-) "f43a8e1b362b75baa741461b46adc7e0")
(setf (get ros_counteruav::fakedata :datatype-) "ros_counteruav/fakedata")
(setf (get ros_counteruav::fakedata :definition-)
      "uint8[] data
")



(provide :ros_counteruav/fakedata "f43a8e1b362b75baa741461b46adc7e0")


