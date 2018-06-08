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
BUFFERSIZE = 160
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))

logging.info("Listening on %s:%d", HOST, PORT)
# TODO temp code that repeatedly logs data from any connecting host
while 1:
    s.listen(1)
    connection, address = s.accept()
    logging.info('Incoming connection from %s', address)
    while 1:
        
        rawdata = connection.recv(BUFFERSIZE)
        print(rawdata)
        logging.info('%s', rawdata)
        if(sys.getsizeof(rawdata) > 0):
            data = bitstring.ConstBitStream(bytes=rawdata, length=160)
            print(data)
            logging.info('%s', data) 

            messageSize = data.read('intle:16')
            logging.info("Received Message Size: %d", messageSize)

            messageType = data.read('intle:16')
            logging.info("Received Message Type: %d", messageType)

            messageTime = data.read('intle:64')
            logging.info("Received Message Time: %d", messageTime)
        
    # RA: 
    #ant_pos = data.bitpos
    #rightAscension = data.read('hex:32')
    #data.bitpos = ant_pos
            rightAscension_uint = data.read('uintle:32')
            logging.info("Destination Right Ascension: %d", rightAscension_uint)
    
    # DEC:
    #ant_pos = data.bitpos
    #declination = data.read('hex:32')
    #data.bitpos = ant_pos
            declination_int = data.read('intle:32')
        logging.info("Destination Declination: %d", declination_int)
    #remember to send coords back to stellarium 10 times in a row
    #connection.close()
