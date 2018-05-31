#!/usr/bin/python2
import sys, argparse, logging, logging.config, socket

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
    while 1:
        data = connection.recv(BUFFERSIZE)
        if not data: break
        logging.info(data)
    connection.close()