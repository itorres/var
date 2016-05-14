#! /bin/sh
env guile -s $0 ${1+"$@"}
exit
!#
(display "Hello, world!")
(newline)
