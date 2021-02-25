#!/usr/bin/env python
import os
import signal
import time
logfile="/tmp/daemon.log"
pid=os.fork()
#exit parent process
if pid: exit()
#get the pid of subprocess
daeid=os.getpid()
os.setsid()
os.umask(0)
os.chdir("/")
#Redirection file descriptor
fd=open("/dev/null","a+")
os.dup2(fd.fileno(),0)
os.dup2(fd.fileno(),1)
os.dup2(fd.fileno(),2)
fd.close()
log=open(logfile,'a')
log.write('Daemon start up at %s\n'%(time.strftime('%Y:%m:%d',time.localtime(time.time()))))
log.close()
def reload(a,b):
  log=open(logfile,'a')
  log.write('Daemon reload at %s\n'%(time.strftime('%Y:%m:%d',time.localtime(time.time()))))
  log.close()
while True:
  signal.signal(signal.SIGHUP,reload)
  time.sleep(2)
 
