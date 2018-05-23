
import time

#!/usr/bin/python
#import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_Stepper
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

import time
import atexit

# define both motor HATs
mh = Adafruit_MotorHAT(addr=0x60)
mh2 = Adafruit_MotorHAT(addr=0x61)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	for i in range(1,4)
		mh.getMotor(i).run(Adafruit_MotorHAT.RELEASE)
	for i in range(1,4)
		mh2.getMotor(i).run(Adafruit_MotorHAT.RELEASE)
	
	'''
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
	mh2.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh2.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh2.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh2.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
	'''

atexit.register(turnOffMotors)

angle = mh2.getStepper(1400, 1) # 1400 steps/rev, motor port #1
rotation = mh2.getStepper(1400, 2) # 1400 steps/rev, motor port #2
focus = mh.getStepper(4096, 2) # 4096 steps/rev, motor port #2
focus.setSpeed(30) # set power to 30 (max: 255)
angle.setSpeed(30) # set power to 30 (max: 255)
rotation.setSpeed(30) # set power to 30 (max: 255)


import sys, termios, tty, os, time

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


while True:
    char = getch()

    if (char == "q"):
        print("Stopping...")
        exit(0)

    elif (char == "t"):
        print(" ")
        focus.step(1, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)

    elif (char == "g"):
        print(" ")
        focus.step(1, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE)

    elif (char == "r"):
        print(" ")
        rotation.step(1, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE)

    elif (char == "y"):
        print(" ")
        rotation.step(1, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)

    elif (char == "f"):
        print(" ")
        angle.step(1, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)

    elif (char == "h"):
        print(" ")
        angle.step(1, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE)


