#!/usr/bin/env python
from socket import *
import json
import leveldb

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

try:
    db = leveldb.LevelDB('/tmp/testdb')
except e:
    print '>>> test : ' + str(e)

while True:
    print ">>> waiting for connection..."
    tcpCliSock, addr = tcpSerSock.accept()
    print '>>> connected by  ' ,addr
    
    while True:
        receive = tcpCliSock.recv(BUFSIZ)
        if not receive:
            break
        data = json.loads(receive)
        print data.keys()
        if  data['index'] == 'upload':
            db.Put(data['filename'],data['filedata'])
            batch = leveldb.WriteBatch()
            db.Write(batch, sync = True)
            send = 'success'
        tcpCliSock.send('%s' %  send)
        print '>>> connection finish!'
        #tcpCliSock.close()
tcpSerSock.close()
