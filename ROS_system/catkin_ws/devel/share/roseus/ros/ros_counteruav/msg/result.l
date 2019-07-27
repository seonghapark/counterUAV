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
    ((:data __data) (make-array 0 :initial-element 0 :element-type :char))
    ((:time __time) (make-array 0 :initial-element 0 :element-type :char))
    )
   (send-super :init)
   (setq _data __data)
   (setq _time __time)
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
    ;; uint8[] _data
    (* 1    (length _data)) 4
    ;; uint8[] _time
    (* 1    (length _time)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8[] _data
     (write-long (length _data) s)
     (princ _data s)
     ;; uint8[] _time
     (write-long (length _time) s)
     (princ _time s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8[] _data
   (let ((n (sys::peek buf ptr- :integer))) (incf ptr- 4)
     (setq _data (make-array n :element-type :char))
     (replace _data buf :start2 ptr-) (incf ptr- n))
   ;; uint8[] _time
   (let ((n (sys::peek buf ptr- :integer))) (incf ptr- 4)
     (setq _time (make-array n :element-type :char))
     (replace _time buf :start2 ptr-) (incf ptr- n))
   ;;
   self)
  )

(setf (get ros_counteruav::result :md5sum-) "27432271eaeca018008ff2d4a194b77d")
(setf (get ros_counteruav::result :datatype-) "ros_counteruav/result")
(setf (get ros_counteruav::result :definition-)
      "uint8[] data
uint8[] time

")



(provide :ros_counteruav/result "27432271eaeca018008ff2d4a194b77d")


