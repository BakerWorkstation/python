#!/usr/bin/env python

from socket import *
import json

HOST = '10.255.40.246'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)



tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    #data = raw_input('> ')
    testdict={"filename":"11","filedata":"asasss","index":"upload"}
    send = json.dumps(testdict)
    tcpCliSock.send(send)

    receive = tcpCliSock.recv(BUFSIZ)
        
    if not receive:
        break
    print receive
    break
tcpCliSock.close()
