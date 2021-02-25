# -*- encoding: utf-8 -*- 
 
import socket 
import select 
 
host = ""
port = 50000  
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
s.bind((host,port))  
s.listen(5) 
s.setblocking(0)
print "begin..." 
while 1:  
    infds,outfds,errfds = select.select([s,],[],[],5)  
    # 如果infds状态改变,进行处理,否则不予理会  
    if len(infds) != 0:  
        clientsock,clientaddr = s.accept() 
        infds_c,outfds_c,errfds_c = select.select([clientsock,],[],[],3) 
        while len(infds_c) != 0:  
            buf = clientsock.recv(8196)  
            #infds_d,outfds_d,errfds_d = select.select([,],[],[],3) 
            if len(buf) != 0:  
                print buf 
            else:
                break
        #else:
        #    clientsock.close() 
        #    break
        #    print "clientsock closed" 
    print "no data coming"