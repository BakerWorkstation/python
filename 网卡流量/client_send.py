# -*- coding:UTF-8 -*-
import datetime
import time
import sys
import functools

list1 = ['adMin', 'toM', 'JeRRy']

print reduce(lambda x,y: ''.join((x, y)), map(lambda z: z.lower().capitalize(), list1))


def log(flag):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            #print '%s : call %s()' % (flag, func.__name__)
            return func(*args, **kw)
        return wrapper
    return decorator

@log('test')
def now(flag):
    print '%s : %s' % (flag, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #sys.stdout.flush()

#while 1:
now('nowtime')
print now.__name__
#time.sleep(1)


import json
import time
import os
import sys
from socket import *


class send():
    def __init__(self, HOST, PORT, FILE, BUFSIZE):
        self.host = HOST
        self.port = PORT
        self.file = FILE
        self.bufsiz = BUFSIZE
        self.handle()
    def handle(self):
        sum = ''
        ff = open(self.file, 'r')
        for i in ff.readlines():
            sum += i
        ff.close()
        testdict={
                   "filename" : self.file,
                   "filedata" : sum
                 }
        #send = json.dumps(testdict)
        send = sum

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
        file1 = sys.argv[3]
    except:
        print '''
        \033[31mWarning : command not right!\033[0m

        \033[32m(HELP)
              parameter 1 :  ip_address
              parameter 2 :  port
              parameter 3 :  filepath

              For example :  " python  client.py  127.0.0.1  50000  /etc/rc.local "\033[0m
              '''
        os._exit(0)
    send(address, int(port), file1, 1024)
