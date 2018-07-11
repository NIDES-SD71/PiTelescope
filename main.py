#!/usr/bin/python3
import sys, argparse, logging, logging.config, socket, struct#, sense_hat
#from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

parser = argparse.ArgumentParser()
parser.add_argument("port", help="Port to listen on", type=int)
parser.add_argument("--host", help="IP to listen on")
args = parser.parse_args()

logging.config.fileConfig('logging.ini')

# TODO probably needs to be moved to other file eventually
HOST = args.host
if(HOST == None):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send 
    HOST = s.getsockname()[0]

PORT = args.port # TODO validate port
BUFFERSIZE = 160
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))

# TODO temp code that repeatedly logs data from any connecting host
try:
    while 1:
        logging.info("Listening on %s:%d", HOST, PORT)
        s.listen(1)
        connection, address = s.accept()
        logging.info('Incoming connection from %s', address)
        try:
            while 1:
                data = connection.recv(BUFFERSIZE)
                #rawSize = sys.getsizeof(data) 
                logging.debug('Data received: %s', data)
                #TODO implement checking for ending message
                #TODO add back in length checking
                #if(rawSize != 20):
                #    logging.debug('Rejected')
                #    continue

                logging.debug('Accepted')
        
                messageSize = struct.unpack("<h", data[0:2])[0]
                logging.info("Received Message Size: %d", messageSize)

                messageType = struct.unpack("<h", data[2:2])[0]
                logging.info("Received Message Type: %d", messageType)
        
                messageTime = struct.unpack("<q", data[4:8])[0]
                logging.info("Received Message Time: %d", messageTime)
        
                rightAscension = struct.unpack("<I", data[12:4])[0]
                logging.info("Destination Right Ascension: %d", rightAscension)

                declination = struct.unpack("<i", data[16:4])[0]
                logging.info("Destination Declination: %d", declination)
    
                #remember to send coords back to stellarium 10 times in a row
        except (KeyboardInterrupt): #May end up needing to explicitly state KeyboardInterrupt; Needs further testing
            connection.close()
except (KeyboardInterrupt):
    connection.close()