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
  :slots (_data _time _num ))

(defmethod ros_counteruav::result
  (:init
   (&key
    ((:data __data) (make-array 0 :initial-element 0 :element-type :char))
    ((:time __time) (make-array 0 :initial-element 0 :element-type :char))
    ((:num __num) 0)
    )
   (send-super :init)
   (setq _data __data)
   (setq _time __time)
   (setq _num (round __num))
   self)
  (:data
   (&optional __data)
   (if __data (setq _data __data)) _data)
  (:time
   (&optional __time)
   (if __time (setq _time __time)) _time)
  (:num
   (&optional __num)
   (if __num (setq _num __num)) _num)
  (:serialization-length
   ()
   (+
    ;; uint8[] _data
    (* 1    (length _data)) 4
    ;; uint8[] _time
    (* 1    (length _time)) 4
    ;; uint64 _num
    8
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
     ;; uint64 _num
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _num (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _num) (= (length (_num . bv)) 2)) ;; bignum
              (write-long (ash (elt (_num . bv) 0) 0) s)
              (write-long (ash (elt (_num . bv) 1) -1) s))
             ((and (class _num) (= (length (_num . bv)) 1)) ;; big1
              (write-long (elt (_num . bv) 0) s)
              (write-long (if (>= _num 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _num s)(write-long (if (>= _num 0) 0 #xffffffff) s)))
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
   ;; uint64 _num
     
#+(or :alpha :irix6 :x86_64)
      (setf _num (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _num (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;;
   self)
  )

(setf (get ros_counteruav::result :md5sum-) "b63e34e765078eeb693def0570c34795")
(setf (get ros_counteruav::result :datatype-) "ros_counteruav/result")
(setf (get ros_counteruav::result :definition-)
      "uint8[] data
uint8[] time
uint64 num

")



(provide :ros_counteruav/result "b63e34e765078eeb693def0570c34795")


