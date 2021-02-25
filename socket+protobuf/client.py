#!/usr/bin/env python

import json
import base64
import addressbook_pb2  
from socket import *

def handle():
    def PromptForAddress(person):
        #person = addressbook_pb2.Person()  
        person.id = int(raw_input('your id: '))
        person.name = raw_input('your name: ').capitalize()
        person.email = raw_input('your email:').lower()
        phone = person.phone.add()  
        phone.number = raw_input('your telephone:')  
        phone.type = addressbook_pb2.Person.HOME  
        #data = str(person)
    address_book = addressbook_pb2.AddressBook()
    PromptForAddress(address_book.person.add())
    data = address_book.SerializeToString()
    
    def send2server(data):
        a = base64.b64encode(data)
        middle={}
        middle['data'] = a
        middle = json.dumps(middle)

        HOST = '10.255.40.245'
        PORT = 21567
        BUFSIZ = 1024
        ADDR = (HOST, PORT)
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        tcpCliSock.send(middle)
        tcpCliSock.close()
    send2server(data)

if  __name__ == '__main__':
    handle()
