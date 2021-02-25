#!/usr/bin/env python

import socket  
import sys  
import json
  
# Create a UDS socket  
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)  
  
# Connect the socket to the port where the server is listening  
server_address = '/dev/shm/ipc.fd'  
print >>sys.stderr, '>>> connecting to %s' % server_address  
try:  
    sock.connect(server_address)  
except socket.error, msg:  
    print >>sys.stderr, msg  
    sys.exit(1)  
try:  
      
    # Send data  
    message = 'This is the message.  It will be repeated.'  
    print >>sys.stderr, '>>> sending "%s"' % message  
    #sock.sendall(raw_input('> '))
    
    testdict=[{"filename":"11","filedata":"asasss","index":"111"}]
    send = json.dumps(testdict)
    print send
    data1 = json.loads(send)
    sock.sendall(send)  
    
    #amount_received = 0  
    #amount_expected = len(message)  
      
    data = sock.recv(1024)
    #amount_received += len(data)  
    print >>sys.stderr, '>>> received "%s"' % data  
  
finally:  
    print >>sys.stderr, '>>> closing socket'  
    sock.close()  
