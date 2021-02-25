#!/usr/bin/python  
#-*- coding: UTF-8 -*-  
# cheungmine  
# stdin、stdout和stderr分别表示子程序的标准输入、标准输出和标准错误。  
#   
# 可选的值有:  
#   subprocess.PIPE - 表示需要创建一个新的管道.  
#   一个有效的文件描述符（其实是个正整数）  
#   一个文件对象  
#   None - 不会做任何重定向工作，子进程的文件描述符会继承父进程的.  
#   
# stderr的值还可以是STDOUT, 表示子进程的标准错误也输出到标准输出.  
#   
# subprocess.PIPE  
# 一个可以被用于Popen的stdin、stdout和stderr 3个参数的特输值，表示需要创建一个新的管道.  
#   
# subprocess.STDOUT  
# 一个可以被用于Popen的stderr参数的特输值，表示子程序的标准错误汇合到标准输出.  
################################################################################  
import os  
import sys  
import getopt  
  
import time  
import datetime  
  
import codecs  
  
import optparse  
import ConfigParser  
  
import signal  
import subprocess  
import select  
  
# logging  
# require python2.6.6 and later  
import logging    
from logging.handlers import RotatingFileHandler  
  
## log settings: SHOULD BE CONFIGURED BY config  
LOG_PATH_FILE = "./my_service_mgr.log"  
LOG_MODE = 'a'  
LOG_MAX_SIZE = 4*1024*1024 # 4M per file  
LOG_MAX_FILES = 4          # 4 Files: my_service_mgr.log.1, printmy_service_mgrlog.2, ...    
LOG_LEVEL = logging.DEBUG    
  
LOG_FORMAT = "%(asctime)s %(levelname)-10s[%(filename)s:%(lineno)d(%(funcName)s)] %(message)s"    
  
handler = RotatingFileHandler(LOG_PATH_FILE, LOG_MODE, LOG_MAX_SIZE, LOG_MAX_FILES)  
formatter = logging.Formatter(LOG_FORMAT)  
handler.setFormatter(formatter)  
  
Logger = logging.getLogger()  
Logger.setLevel(LOG_LEVEL)  
Logger.addHandler(handler)   
  
# color output  
#  
pid = os.getpid()   
  
def print_error(s):  
    print '\033[31m[%d: ERROR] %s\033[31;m' % (pid, s)  
  
def print_info(s):  
    print '\033[32m[%d: INFO] %s\033[32;m' % (pid, s)  
  
def print_warning(s):  
    print '\033[33m[%d: WARNING] %s\033[33;m' % (pid, s)  
  
  
def start_child_proc(command, merged):  
    try:  
        if command is None:  
            raise OSError, "Invalid command"  
  
        child = None  
  
        if merged is True:  
            # merge stdout and stderr  
            child = subprocess.Popen(command,  
                stderr=subprocess.STDOUT, # 表示子进程的标准错误也输出到标准输出  
                stdout=subprocess.PIPE    # 表示需要创建一个新的管道  
            )  
        else:  
            # DO NOT merge stdout and stderr  
            child = subprocess.Popen(command,  
                stderr=subprocess.PIPE,  
                stdout=subprocess.PIPE)  
  
        return child  
  
    except subprocess.CalledProcessError:  
        pass # handle errors in the called executable  
    except OSError:  
        pass # executable not found  
  
    raise OSError, "Failed to run command!"  
  
  
def run_forever(command):  
    print_info("start child process with command: " + ' '.join(command))  
    #Logger.info("start child process with command: " + ' '.join(command))  
  
    merged = False  
    child = start_child_proc(command, merged)  
  
    line = ''  
    errln = ''  
  
    failover = 0  
  
    while True:  
        while child.poll() != None:  
            failover = failover + 1  
            print_warning("child process shutdown with return code: " + str(child.returncode))             
            Logger.critical("child process shutdown with return code: " + str(child.returncode))  
  
            print_warning("restart child process again, times=%d" % failover)  
            Logger.info("restart child process again, times=%d" % failover)  
            child = start_child_proc(command, merged)  
  
        # read child process stdout and log it  
        ch = child.stdout.read(1)  
        if ch != '' and ch != '\n':  
            line += ch  
        if ch == '\n':  
            print_info(line)  
            line = ''  
  
        if merged is not True:  
            # read child process stderr and log it  
            ch = child.stderr.read(1)  
            if ch != '' and ch != '\n':  
                errln += ch  
            if ch == '\n':  
                Logger.info(errln)  
                print_error(errln)  
                errln = ''  
  
    Logger.exception("!!!should never run to this!!!")    
  
  
if __name__ == "__main__":  
    run_forever(["python", "./client.py"])  
