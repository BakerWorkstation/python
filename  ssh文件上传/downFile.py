#!/usr/bin/python

import os
import time

server = {
          'web1' :  15174,
          'web2' :  15175,
          'web3' :  15176,
          'api1' :  15170,
          'api2' :  15171,
          'task1':  15172,
          'task2':  15173
         }

def handle(port, filename):
    cmd = "/usr/local/bin/rsync  -IP --rsh=ssh  -e 'ssh -p %s'  XSPLZ@127.0.0.1:/home/XSPLZ/%s   /Users/songdancheng/Downloads/" % (port, filename)
    os.system(cmd)

def main():
    port = server['api1']
    filename = 'api.zip'
    handle(port, filename)
    
    
if __name__ == '__main__':
    main()