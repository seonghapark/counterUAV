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
  :slots (_data _num ))

(defmethod ros_counteruav::fakedata
  (:init
   (&key
    ((:data __data) (make-array 0 :initial-element 0 :element-type :char))
    ((:num __num) 0)
    )
   (send-super :init)
   (setq _data __data)
   (setq _num (round __num))
   self)
  (:data
   (&optional __data)
   (if __data (setq _data __data)) _data)
  (:num
   (&optional __num)
   (if __num (setq _num __num)) _num)
  (:serialization-length
   ()
   (+
    ;; uint8[] _data
    (* 1    (length _data)) 4
    ;; uint8 _num
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8[] _data
     (write-long (length _data) s)
     (princ _data s)
     ;; uint8 _num
       (write-byte _num s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8[] _data
   (let ((n (sys::peek buf ptr- :integer))) (incf ptr- 4)
     (setq _data (make-array n :element-type :char))
     (replace _data buf :start2 ptr-) (incf ptr- n))
   ;; uint8 _num
     (setq _num (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get ros_counteruav::fakedata :md5sum-) "779cd9dc2f41ba0741e7ebbe961855fd")
(setf (get ros_counteruav::fakedata :datatype-) "ros_counteruav/fakedata")
(setf (get ros_counteruav::fakedata :definition-)
      "uint8[] data
uint8   num
")



(provide :ros_counteruav/fakedata "779cd9dc2f41ba0741e7ebbe961855fd")


