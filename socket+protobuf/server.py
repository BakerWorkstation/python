#!/usr/bin/env python
#! -*- coding:utf-8 -*-

import json
import base64
from socket import *
import addressbook_pb2
HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
while True:
    print ">>> waiting for connection..."
    tcpCliSock, addr = tcpSerSock.accept()
    print '>>> connected by  ' ,addr
    receive = tcpCliSock.recv(BUFSIZ)
    #tcpCliSock.send('%s' %  send)
    #tcpSerSock.close()
    data = base64.b64decode(json.loads(receive)['data'])
    address_book = addressbook_pb2.AddressBook()
    address_book.ParseFromString(data)
    print address_book
    #for person in  address_book.person:
    #    print person.id
    #    print person.name
    #    print person.email
    #    print person.phone
