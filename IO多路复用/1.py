__author__ = 'BurNing'
# -*- coding:UTF-8 -*-

import select
#导入select模块
BLKSIZE=8192

def readwrite(fromfd,tofd):
    readbuf = fromfd.read(BLKSIZE)
    if readbuf:
        tofd.write(readbuf)
        tofd.flush()
    return len(readbuf)

def copy2file(fromfd1,tofd1,fromfd2,tofd2):
    ''' using select to choice fds'''
    totalbytes=0
    if not (fromfd1 or fromfd2 or tofd1 or tofd2) :
 #检查所有文件描述符是否合法
        return 0
    i, j = 1, 1
    while True:
 #开始利用select对输入所有输入的文件描述符进行监视
        #print 'fromdf1 : %s' % fromfd1
        #print 'fromfd2 : %s' % fromfd2
        rs,ws,es = select.select([fromfd1,fromfd2],[],[])
        for r in rs:
            if r is fromfd1:
                bytesread = readwrite(fromfd1,tofd1)
                if bytesread == 0:
                     i = 0
                totalbytes += bytesread
            if r is fromfd2:
                bytesread = readwrite(fromfd2,tofd2)
                if bytesread == 0:
                     j = 0
                totalbytes += bytesread
        if  i | j == 0:
            break
    return totalbytes

def main():
    fromfd1 = open("./500M","r")
    fromfd2 = open("./1G","r")
    tofd1 = open("./new_500M","w+")
    tofd2 = open("./new_1G","w+")
    totalbytes = copy2file(fromfd1,tofd1,fromfd2,tofd2)
    print "Number of bytes copied %d\n" % totalbytes
    return 0

if __name__=="__main__":
    main()
