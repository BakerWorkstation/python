__author__ = 'BurNing'
# -*- coding:utf-8 -*-

import multiprocessing
import time

def proc1(pipe, i):

    print u"proc1 发送: %s \n" % i
    pipe.send(i)
    time.sleep(1)

def proc2(pipe):
    print u'proc2 接收: %s\n' % pipe.recv()
    time.sleep(1)

def proc3(pipe):
    while True:
        print u'proc3 接收: %s\n' % pipe.recv()
        time.sleep(1)
        # Build a pipe
pipe = multiprocessing.Pipe()
#print pipe

# Pass an end of the pipe to process 1
p1 = multiprocessing.Process(target=proc1, args=(pipe[0], 20))
# Pass the other end of the pipe to process 2
p2 = multiprocessing.Process(target=proc2, args=(pipe[1], ))


p1.start()
p2.start()
p1.join()
p2.join()