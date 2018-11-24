import sys, logging, threading
from sense_hat import SenseHat
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor

class MotorController:
    sense = SenseHat()

    def __move(self):
        while 1:
            [currentYaw, currentRoll, currentPitch] = self.sense.get_orientation_degrees().values()
            #Each .step() only steps by 1 to avoid any one movement blocking all others
            if (self.YawMotor != None and currentYaw != self.DestYaw):
                self.YawMotor.step(1, Adafruit_MotorHAT.FORWARD if bool(currentYaw < self.DestYaw) ^ self.InvertYaw else Adafruit_MotorHAT.BACKWARD, self.YawPower)
                logging.debug("yaw: %s", currentYaw)
            if (self.PitchMotor != None and currentPitch != self.DestPitch):
                self.PitchMotor.step(1, Adafruit_MotorHAT.FORWARD if bool(currentPitch < self.DestPitch) ^ self.InvertPitch else Adafruit_MotorHAT.BACKWARD, self.PitchPower)
                logging.debug("pitch: %s", currentPitch)
            if (self.RollMotor != None and currentRoll != self.DestRoll):
                self.RollMotor.step(1, Adafruit_MotorHAT.FORWARD if bool(currentRoll < self.DestRoll) ^ self.InvertRoll else Adafruit_MotorHAT.BACKWARD, self.RollPower)
                logging.debug("roll: %s", currentRoll)

    def StartMove(self):
        if(self.__moveThread is None):
            self.__moveThread = threading.Thread(target=self.__move)
            self.__moveThread.start

    def StopMove(self):
        if(self.__moveThread is not None):
            self.__moveThread.join(1)
        self.__moveThread = None

    def __init__(self, yawMotor, pitchMotor, rollMotor, destYaw = 0, destPitch = 0, destRoll = 0, invertYaw = False, invertPitch = False, invertRoll = False, yawPower = Adafruit_MotorHAT.SINGLE, pitchPower = Adafruit_MotorHAT.SINGLE, rollPower = Adafruit_MotorHAT.SINGLE):
        self.YawMotor = yawMotor or None
        self.YawPower = yawPower
        self.InvertYaw = invertYaw
        self.DestYaw = destYaw

        self.PitchMotor = pitchMotor or None
        self.PitchPower = pitchPower
        self.InvertPitch = invertPitch
        self.DestPitch = destPitch
        
        self.RollMotor = rollMotor or None
        self.RollPower = rollPower
        self.InvertRoll = invertRoll
        self.DestRoll = destRoll
        self.__moveThread