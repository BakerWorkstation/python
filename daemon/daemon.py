#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#-------------------------------------------------------------
#  __author__ : Sylar
#       Timer : 2016/09/08
#    function : daemon program
#-------------------------------------------------------------

import os
import sys
import time
import json
import socket
import select
import ctypes
import threading
import subprocess

from mod_config import ParseConfig


class DaemonP(threading.Thread):

    def __init__(self, command):
        threading.Thread.__init__(self)
        self.__IDE = command.strip().split(' ')[0]
        self.__service = command.strip().split(' ')[-1]
        self.ifdo = True
        self.p = ''

    def run(self):
        #print ctypes.CDLL('libc.so.6').syscall(186)
        flag = True
        while self.ifdo:
            if not flag == None:
                self.p = subprocess.Popen([
                                          self.__IDE, self.__service],
                                          stdout=subprocess.PIPE)
            flag = self.p.poll()
            time.sleep(0.1)

    def stop(self):
        self.ifdo = False
        self.p.kill()

def mainloop(path):
    start_list = {}
    stop_list = []
    P = ParseConfig(path)
    for eachsection in P.getsection():
        flag = P.getconfig(eachsection)[0]
        command = P.getconfig(eachsection)[1]
        if flag == '1':
            b = DaemonP(command)
            b.setDaemon(True)
            b.start()
            start_list[eachsection] = b
        else:
            stop_list.append(eachsection)

    HOST = ""
    PORT = 50000
    s = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)
    s.bind((
            HOST,
            PORT))
    s.listen(5)
    s.setblocking(0)

    while True:
        infds,outfds,errfds = select.select([
                                            s,],
                                            [],
                                            [],
                                            5)
        sum = ''
        if len(infds) != 0:
            clientsock,clientaddr = s.accept()
            infds_c,outfds_c,errfds_c = select.select([
                                                      clientsock,],[],[],
                                                      3)
            while len(infds_c) != 0:
                buf = clientsock.recv(8192)
                if len(buf) != 0:
                    sum += buf
                else:
                    print 'info :', sum
                    info = json.loads(sum)
                    key1 = info.keys()[0]
                    value = info[key1]

                    if value == '1':
                        if key1 in start_list.keys():
                            print '\033[37;31;5m  service\
 has been start !\033[39;49;0m'
                        elif key1 in stop_list:
                            command = P.getcommand(key1)
                            b = DaemonP(command)
                            b.setDaemon(True)
                            b.start()
                            start_list[key1] = b
                            stop_list.remove(key1)
                            print '\033[37;32;5m  service\
  start !\033[39;49;0m'
                        else:
                            print '\033[37;31;5m  no such\
 service !\033[39;49;0m'
                        break

                    if value == '0':
                        if key1 in start_list.keys():
                            start_list[key1].stop()
                            start_list.pop(key1)
                            stop_list.append(key1)
                            print '\033[37;32;5m  service\
  stop !\033[39;49;0m'
                        elif key1 in stop_list:
                            print '\033[37;31;5m  service\
  has been stop !\033[39;49;0m'
                        else:
                            print '\033[37;31;5m  no such\
 service !\033[39;49;0m'
                        break


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except:
        print '''
        \033[31mWarning : command not right!\033[0m

        \033[32m(HELP)
              parameter 1 :  config_file

              For example :  " python  daemon.py  /tmp/define.cfg "\033[0m
              '''
        os._exit(0)
    mainloop(path)
