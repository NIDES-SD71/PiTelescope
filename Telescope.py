# Simple two DC motor robot class usage example.
# Author: Tony DiCola
# License: MIT License https://opensource.org/licenses/MIT
import time

#!/usr/bin/python
#import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_Stepper
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)
mh2 = Adafruit_MotorHAT(addr=0x61)

# recommended for auto-disabling motors on shutdown!

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

angle = mh2.getStepper(1400, 1)
rotation = mh2.getStepper(1400, 2)
focus = mh.getStepper(4096, 2)  # 200 steps/rev, motor port #1
focus.setSpeed(30) # 30 RPM
angle.setSpeed(30)
rotation.setSpeed(30)
# Set the trim offset for each motor (left and right).  This is a value that
# will offset the speed of movement of each motor in order to make them both
# move at the same desired speed.  Because there's no feedback the robot doesn't
# know how fast each motor is spinning and the robot can pull to a side if one
# motor spins faster than the other motor.  To determine the trim values move t$
# robot forward slowly (around 100 speed) and watch if it veers to the left or
# right.  If it veers left then the _right_ motor is spinning faster so try
# robot forward slowly (around 100 speed) and watch if it veers to the left or
# right.  If it veers left then the _right_ motor is spinning faster so try
# setting RIGHT_TRIM to a small negative value, like -5, to slow down the right
# motor.  Likewise if it veers right then adjust the _left_ motor trim to a sma$
# negative value.  Increase or decrease the trim value until the bot moves
# straight forward/backward.


# Create an instance of the robot with the specified trim values.
# Not shown are other optional parameters:
#  - addr: The I2C address of the motor HAT, default is 0x60.
#  - left_id: The ID of the left motor, default is 1.
#  - right_id: The ID of the right motor, default is 2.

# Now move the robot around!
# Each call below takes two parameters:
# Now move the robot around!
# Each call below takes two parameters:
#  - speed: The speed of the movement, a value from 0-255.  The higher the value
#           the faster the movement.  You need to start with a value around 100
#           to get enough torque to move the robot.
#  - time (seconds):  Amount of time to perform the movement.  After moving for
#                     this amount of seconds the robot will stop.  This paramet$
#                     is optional and if not specified the robot will start mov$
#                     forever

#!/usr/bin/python3

# adapted from https://github.com/recantha/EduKit3-RC-Keyboard/blob/master/rc_k$

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


