#! -*- coding:utf-8 -*-
import os    
import signal    
from time import sleep    
     
def onsigchld(a,b):    
    print '收到子进程结束信号'    

signal.signal(signal.SIGCHLD,onsigchld)    

pid = os.fork()    
if pid == 0:    
    print '我是子进程,pid是',os.getpid()    
    try:
        sleep(20)
    except KeyboardInterrupt:
        sleep(20)
else:    
    print '我是父进程,pid是',os.getpid()    
    try:
        os.wait()  #等待子进程结束  
    except KeyboardInterrupt:
        pass
