import time
from sense_hat import SenseHat

while(True):
    sense = SenseHat()
    orientation_rad = sense.get_orientation_radians()
    print("pitch: {pitch}".format(**orientation_rad))
    print("roll: {roll}".format(**orientation_rad))
    print("yaw: {yaw}".format(**orientation_rad))
    print(" ")

