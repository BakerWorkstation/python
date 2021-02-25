#!/usr/bin/env python
import socket  
import sys  
import os  
import leveldb
import json
import base64
import threading
import datetime
from Queue import Queue
#reload(sys)
#sys.setdefaultencoding('utf-8')

def configuration():
    global queue,sock,database,db,id
    id = 0
    queue = Queue()
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
    print >>sys.stderr, 'starting up on "%s"' % server_address  
    sock.bind(server_address)  
    sock.listen(10)  

    # Listen for incoming connections  
    try:
        database = '/tmp/testdb'
        db = leveldb.LevelDB(database)
    except Exception as e:
        print 'leveldb : ' + str(e)


class TaskThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        t = queue.get()
            # Wait for a connection  
        print '\n' + '>'*20 + 'connection build\n'
        sum = ''

        try:
            while True:  
                receive = t.recv(26000)
                sum = sum + receive
                if receive[-1] == '}':
                    receive = sum
                    break
        except Exception as e:
            print 'receive : ' , str(e)

        data = json.loads(receive)
        data['filedata'] = base64.b64decode(data['filedata'])

        if data['index']  ==  'upload':
            #print '\n' + '-'*25,'>  Receive Start !  <','-'*25 + '\n'
            print '-' * 50
            print 'id        :  %d'  %  id
            print 'datetime  :  %s'  %  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print 'filename  :  %s'  %  data['filename']
            print 'filesize  :  %s'  %  int(round(float(len(data['filedata']))/float(1024))),'KB'
            print 'operate   :  %s'  %  data['index']
            print 'location  :  %s'  %  database
            print '-' * 50
            #print '\n' + '-'*25,'>  Receive  Over !  <','-'*25 + '\n'
            db.Put(data['filename'] ,data['filedata'])
            send = 'success'
            print >>sys.stderr, '~~~  Sending data back to the client ...',
            t.sendall(send)
            #print >>sys.stderr, '\t\tOK'  

        if data['index'] == 'download':
            #print data['filename']
            content = db.Get(data['filename'])#.decode(encoding = 'utf-8')
            #print len(content)
            content = base64.b64encode(content)
            download = { 'body' : content }
            print str(download)[-10:]
            download = json.dumps(download)
            print '-' * 50
            #print '\n' + '-'*25,'>  Send  Start !  <','-'*25 + '\n'
            print 'id        :  %d'  %  id
            print 'datetime  :  %s'  %  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print 'filename  :  %s'  %  data['filename']
            print 'filesize  :  %s'  %  int(round(float(len(content))/float(1024))),'KB'
            print 'operate   :  %s'  %  data['index']
            print 'location  :  %s'  %  database
            print '-' * 50
            print >>sys.stderr, '~~~  Sending data back to the client ...',
            #print '\n' + '-'*25,'>  Send   Over !  <','-'*25 + '\n'
            t.sendall(download)

        print >>sys.stderr, '\n\t\t\t\t\tConnection  Over ' + '<'*20 , client_address
        t.close()
    #print >>sys.stderr, '>>>  waiting for a connection ...'  

if __name__ == '__main__' :
    configuration()
    while True:
        connection, client_address = sock.accept()  
        print type(connection)
        queue.put(connection)
        th = TaskThread()
        th.setDaemon(True)
        #print queue
        th.start()
        id += 1
        #queue.join()
