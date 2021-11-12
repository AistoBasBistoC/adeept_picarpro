import time
import threading
import move
import RPIservo
import servo
import Adafruit_PCA9685
import os
import info
import webServer

mark_test = 0

functionMode = 0
speed_set = 100
rad = 0.5
turnWiggle = 60

scGear = RPIservo.ServoCtrl()
scGear.moveInit()

P_sc = RPIservo.ServoCtrl()
P_sc.start()

T_sc = RPIservo.ServoCtrl()
T_sc.start()

H_sc = RPIservo.ServoCtrl()
H_sc.start()

G_sc = RPIservo.ServoCtrl()
G_sc.start()


# test arm move down, grab, arm move up, release (1 sec delays)
T_sc.singleServo(2, -1, 3)  # arm moves down
time.sleep(1)
T_sc.singleServo(2, -1, 0)  # arm stops moving
time.sleep(1)
G_sc.singleServo(4, -1, 3)  # grabber grabs
time.sleep(1)
G_sc.singleServo(4, -1, 0)  # grabber stops
time.sleep(1)
T_sc.singleServo(2, 1, 3)  # arm moves up
time.sleep(1)
T_sc.singleServo(2, 1, 0)  # arm stops
time.sleep(1)
G_sc.singleServo(4, 1, 3)  # grabber releases
time.sleep(1)
G_sc.singleServo(4, 1, 0)  # grabber stops
time.sleep(1)


