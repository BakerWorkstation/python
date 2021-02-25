#!/usr/bin/env python
import socket  
import sys  
import os  
import leveldb
import json
  
server_address = '/dev/shm/ipc.fd'  
  
# Make sure the socket does not already exist  
try:  
    os.unlink(server_address)  
except OSError:  
    if os.path.exists(server_address):  
        raise  
# Create a UDS socket  
sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)  
# Bind the socket to the port  
print >>sys.stderr, 'starting up on %s' % server_address  
sock.bind(server_address)  
  
# Listen for incoming connections  
sock.listen(1)  
try:
    db = leveldb.LevelDB('/tmp/testdb')
except e:
    print 'test : ' + str(e)
  
while True:  
    # Wait for a connection  
    print >>sys.stderr, '>>> waiting for a connection ...'  
    connection, client_address = sock.accept()  
    try:  
        print >>sys.stderr, '>>> connected by localhost !' ,  client_address  
  
        # Receive the data in small chunks and retransmit it  
        while True:  
            receive = connection.recv(1024)
            if not receive :
                break
            data = json.loads(receive)
            print >>sys.stderr, '>>> received data : "%s"' % data  
            print >>sys.stderr, '>>> sending data back to the client ...'  
            connection.sendall('hello client !')
            print >>sys.stderr, '>>> connection finish !', client_address
              
    finally:  
        # Clean up the connection  
        connection.close()
