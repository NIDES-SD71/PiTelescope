#!/usr/bin/python2
import sys, argparse, logging, logging.config, socket, bitstring#, sense_hat
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
while 1:
    logging.info("Listening on %s:%d", HOST, PORT)
    s.listen(1)
    connection, address = s.accept()
    logging.info('Incoming connection from %s', address)
    try:
        while 1:
            rawdata = connection.recv(BUFFERSIZE)
            rawSize = sys.getsizeof(rawdata) 
            logging.debug('Data received: %s', rawdata)
            #TODO implement checking for ending message
            if(rawSize != 20):
                logging.debug('Rejected')
                continue
            logging.debug('Accepted')
        
            data = bitstring.ConstBitStream(bytes=rawdata, length=rawSize * 8)
            logging.debug('Bitstring created: %s', data) 
        
            messageSize = data.read('intle:16')
            logging.info("Received Message Size: %d", messageSize)

            messageType = data.read('intle:16')
            logging.info("Received Message Type: %d", messageType)
        
            messageTime = data.read('intle:64')
            logging.info("Received Message Time: %d", messageTime)
        
            rightAscension = data.read('uintle:32')
            logging.info("Destination Right Ascension: %d", rightAscension)

            declination = data.read('intle:32')
            logging.info("Destination Declination: %d", declination)
    
            #remember to send coords back to stellarium 10 times in a row
    except: #May end up needing to explicitly state KeyboardInterrupt; Needs further testing
        connection.close()
