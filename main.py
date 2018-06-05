#!/usr/bin/python2
import sys, argparse, logging, logging.config, socket, bitstring

parser = argparse.ArgumentParser()
parser.add_argument("port", help="Port to listen on", type=int)
parser.add_argument("--host", help="IP to listen on")
args = parser.parse_args()

logging.config.fileConfig('logging.ini')

# TODO probably needs to be moved to other file eventually
HOST = args.host
if( HOST == None):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send 
    HOST = s.getsockname()[0]

PORT = args.port # TODO validate port
BUFFERSIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))

logging.info("Listening on %s:%d", HOST, PORT)
# TODO temp code that repeatedly logs data from any connecting host
while 1:
    s.listen(1)
    connection, address = s.accept()
    logging.info('Incoming connection from %s', address)

    data = ConstBitStream(bytes=connection.recv(BUFFERSIZE), length=160)
 
    messageSize = data.read('intle:16')
    messageType = data.read('intle:16')
    messageTime = data.read('intle:64')
        
    # RA: 
    #ant_pos = data.bitpos
    #rightAscension = data.read('hex:32')
    #data.bitpos = ant_pos
    rightAscension_uint = data.read('uintle:32')
 
    # DEC:
    #ant_pos = data.bitpos
    #declination = data.read('hex:32')
    #data.bitpos = ant_pos
    declination_int = data.read('intle:32')

    #remember to send coords back to stellarium 10 times in a row
    logging.info("Received Message Size: %d\nReceived Message Type: %d\nReceived Message Time: %d\nDestination Right Ascension: %d\nDestination Declination: %d", messageSize, messageType, messageTime, rightAscension_uint, declination_int)
    connection.close()