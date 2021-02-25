#!/usr/bin/python

import os
import time
import subprocess
from multiprocessing import Pool

weblist = ['15174', '15175', '15176']
apilist = ['15170', '15171']
tasklist = ['15172', '15173']
webdir = '/Users/songdancheng/webfiles'
apidir = '/Users/songdancheng/apifiles'
taskdir = '/Users/songdancheng/taskfiles'

def handle(eachport, eachfile):
    try:
        while 1:
            print eachport
            cmd = "/usr/local/bin/rsync  -IP --rsh=ssh  -e 'ssh -p %s'  %s  XSPLZ@127.0.0.1:/home/XSPLZ/%s" % (eachport, eachfile, eachfile)
            result = os.system(cmd)
            if not result == 0:
                time.sleep(0.5)
            else:
                break
    except Exception, e:
        pass

def web():
    os.chdir(webdir)
    for eachfile in os.listdir('./'):
        if eachfile == '.DS_Store':
            continue
        p = Pool(3)
        for eachport in weblist:
            #handle(eachport, eachfile)
            print('Parent process %s.' % os.getpid())
            p.apply_async(handle, args=(eachport, eachfile,))
        print('Waiting for all subprocesses done...')
        p.close()
        p.join()
        print('All subprocesses done.')
        os.remove(os.path.join(webdir, eachfile))
         
def api():
    os.chdir(apidir)
    for eachfile in os.listdir('./'):
        if eachfile == '.DS_Store':
            continue
        p = Pool(2)
        for eachport in apilist:
            #handle(eachport, eachfile)
            print('Parent process %s.' % os.getpid())
            p.apply_async(handle, args=(eachport, eachfile,))
        print('Waiting for all subprocesses done...')
        p.close()
        p.join()
        print('All subprocesses done.')
        os.remove(os.path.join(apidir, eachfile))

def task():
    os.chdir(taskdir)
    for eachfile in os.listdir('./'):
        if eachfile == '.DS_Store':
            continue
        p = Pool(2)
        for eachport in tasklist:
            #handle(eachport, eachfile)
            print('Parent process %s.' % os.getpid())
            p.apply_async(handle, args=(eachport, eachfile,))
        print('Waiting for all subprocesses done...')
        p.close()
        p.join()
        print('All subprocesses done.')
        os.remove(os.path.join(taskdir, eachfile))
			
if __name__ == '__main__':
	web()
	api()
	task()
