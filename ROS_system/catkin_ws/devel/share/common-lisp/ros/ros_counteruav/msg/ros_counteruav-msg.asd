
(cl:in-package :asdf)

(defsystem "ros_counteruav-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "fakedata" :depends-on ("_package_fakedata"))
    (:file "_package_fakedata" :depends-on ("_package"))
    (:file "objectinfo" :depends-on ("_package_objectinfo"))
    (:file "_package_objectinfo" :depends-on ("_package"))
    (:file "result" :depends-on ("_package_result"))
    (:file "_package_result" :depends-on ("_package"))
    (:file "wav" :depends-on ("_package_wav"))
    (:file "_package_wav" :depends-on ("_package"))
  ))