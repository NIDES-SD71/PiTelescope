#!/usr/bin/python3
from datetime import datetime
from coordinates import coordinates
from sense_hat import SenseHat
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor
from MotorController import MotorController
import sys, argparse, logging, logging.config, socket, struct, time, angles

def angleToStellarium(Ra,Dec):
    return [int(Ra.h*(2147483648/12.0)), int(Dec.d*(1073741824/90.0))]
        
def stellariumToAngle(RaInt,DecInt):
    Ra = angles.Angle(h=(RaInt*12.0/2147483648))
    Dec = angles.Angle(d=(DecInt*90.0/1073741824))
    return [Ra, Dec]

#Load logging config
logging.config.fileConfig('logging.ini')

#Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("port", help="Port to listen on", type=int)
parser.add_argument("--host", help="IP to listen on")
args = parser.parse_args()

#Set arguments
# TODO probably needs to be moved to other file eventually
HOST = args.host
if(HOST == None):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send 
    HOST = s.getsockname()[0]
PORT = args.port # TODO validate port

#Setting up other stuff
BUFFERSIZE = 160
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
mh = Adafruit_MotorHAT(addr=0x60)
mh2 = Adafruit_MotorHAT(addr=0x61)
mc = MotorController(mh2.getStepper(1400, 1), None, mh2.getStepper(1400, 2))

try:
    #Listen for incoming connections
    while 1:
        logging.info("Listening on %s:%d", HOST, PORT)
        s.listen(1)
        connection, address = s.accept()
        logging.info('Incoming connection from %s', address)
        try:
            #Do stuff while connected
            while 1:
                data = connection.recv(BUFFERSIZE)
                rawSize = len(data) 
                logging.debug('Data received: %s', data)
                #TODO implement checking for ending message
                if(rawSize != 20):
                    logging.debug('Rejected (%d != 20)', rawSize)
                    continue
                logging.debug('Accepted')
        
                # Read stellarium stuff
                messageSize,messageType,messageTime,destRightAscension,destDeclination = struct.unpack("<hhqIi", data)
                logging.info("Received Message Size: %d", messageSize)
                logging.info("Received Message Type: %d", messageType)
                logging.info("Received Message Time: %d", messageTime)
                logging.info("Destination Right Ascension: %d", destRightAscension)
                logging.info("Destination Declination: %d", destDeclination)
                
                # Preparing destination
                [destYaw, destRoll] = stellariumToAngle(destRightAscension,destDeclination)
                logging.info("Destination Roll: %d", destRoll.d)
                logging.info("Destination Yaw: %d", destYaw.d)

                # Using destination
                mc.DestRoll = destRoll.d
                mc.DestYaw = destYaw.d
                mc.StartMove()

                #Preparing sendback data
                sense = SenseHat()
                [yaw, roll, pitch] = sense.get_orientation_degrees().values()
                logging.info("pitch: %s", pitch)
                logging.debug("roll: %s", roll)
                logging.info("yaw: %s", yaw)
                
                coords = coordinates(datetime.utcnow())
                [Ra, Dec] = coords.getRaDec(yaw, pitch)
                logging.info("Right Ascension. Degrees: %s. Radians: %s. Hours: %s", Ra.d, Ra.r, Ra.h)
                logging.info("Declination. Degrees: %s. Radians: %s. Hours: %s", Dec.d, Dec.r, Dec.h)

                [RaInt,DecInt] = angleToStellarium(Ra, Dec)
                #"<hhqIi"
                sendbackdata = struct.pack("3iIii", 24, 0, time.time(), RaInt, DecInt,0) 
                for x in range(10):
                    connection.send(sendbackdata)
        except (KeyboardInterrupt):
            connection.close()
            mc.StopMove()
except (KeyboardInterrupt):
    connection.close()