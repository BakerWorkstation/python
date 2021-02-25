#!/usr/bin/env python
# -*- encoding: utf-8 -*- 

#-------------------------------------------------------------   
#  __author__ : Sylar
#       Timer : 2016/09/07
#    function : send file from host_A to host_B (client)
#-------------------------------------------------------------

import json
import os
import sys
from socket import *


class send():
    def __init__(self, HOST, PORT, filename, switch, BUFSIZE):
        self.host = HOST
        self.port = PORT
        self.filename = filename
        self.switch = switch
        self.bufsiz = BUFSIZE
        self.handle()
    def handle(self):
        testdict={ 
                   self.filename : self.switch
                 }
        send = json.dumps(testdict)

        ADDR = (self.host, self.port)
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        while send:
            bytes = tcpCliSock.send(send)
            send = send[bytes:]

        tcpCliSock.close()
        #receive = tcpCliSock.recv(BUFSIZ)
        #if not receive:
        #    break
        #print receive

if  __name__ == '__main__':
    try:
        address = sys.argv[1]
        port = sys.argv[2]
        filename = sys.argv[3]
        switch = sys.argv[4]
    except:
        print '''
        \033[31mWarning : command not right!\033[0m

        \033[32m(HELP)
              parameter 1 :  ip_address
              parameter 2 :  port
              parameter 3 :  filename
              parameter 4 :  switch

              For example :  " python  client_tool.py  127.0.0.1  50000  1.sh 1 "\033[0m
              '''
        os._exit(0)
    send(address, int(port), filename, switch, 1024)
