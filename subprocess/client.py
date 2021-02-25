#!/usr/bin/python  
#-*- coding: UTF-8 -*-  
# cheungmine  
# 模拟一个woker进程,10秒挂掉  
import os  
import sys  
  
import time  
import random  
  
cnt = 10  
  
while cnt >= 0:  
    time.sleep(0.5)  
    sys.stdout.write("OUT: %s\n" % str(random.randint(1, 100000)))  
    sys.stdout.flush()  
  
    time.sleep(0.5)  
    sys.stderr.write("ERR: %s\n" % str(random.randint(1, 100000)))  
    sys.stderr.flush()  
  
    #print str(cnt)  
    #sys.stdout.flush()  
    cnt = cnt - 1  
  
sys.exit(-1)  
