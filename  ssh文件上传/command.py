#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
from pexpect import pxssh
from multiprocessing import Pool

weblist = [{'port': '15174', 'passwd': '1@JF8rguBtw6%XG!'}, 
           {'port': '15175', 'passwd': 'dV14DS@MrU6iOi!d'}, 
           {'port': '15176', 'passwd': 'ub8$d^hLmv9mOb4p'}]

apilist = [{'port': '15170', 'passwd': 'aY2Q^8bF8D$NCkb9'},
           {'port': '15171', 'passwd': 'bK1z%21CaQiVYatO'}]

tasklist = [{'port': '15172', 'passwd': 'evYdYl0Dxlz4WH#&'}]#, '15173']

def send_command(s, cmd, passwd):  
	#s.sendline(cmd)  
	s.sendline ('su -') #切换到root 
	print 'start' 
	s.expect(['Password:'])  
	s.sendline(passwd)#root密码  
	s.prompt()  
	print s.before
	for eachcmd in cmd:
		s.sendline(eachcmd)
		s.prompt()  
	print s.before
	s.sendline('exit')
	s.logout()
	print 'finish'

def connect(host, user, port, cmd, passwd):
	try:  
		s = pxssh.pxssh()
		s.login(host, username=user, port=port)
		send_command(s, cmd, passwd)
		#return s  
	except Exception, e:  
		print str(e)  
		exit(0)
		  
def main():  
	#s = connect('127.0.0.1', 'XSPLZ', '15174')
	#send_command(s, 'netstat -antp | grep  LIST')
	cmd = ['netstat -antp | grep -i estab | wc -l']
	p = Pool(6)
	for eachinfo in weblist:
		#handle(eachport, eachfile)
		print('Parent process %s.' % os.getpid())
		p.apply_async(connect, args=('127.0.0.1', 'XSPLZ', eachinfo['port'], cmd, eachinfo['passwd'], ))
	for eachinfo in apilist:
		#handle(eachport, eachfile)
		print('Parent process %s.' % os.getpid())
		p.apply_async(connect, args=('127.0.0.1', 'XSPLZ', eachinfo['port'], cmd, eachinfo['passwd'], ))
	for eachinfo in tasklist:
		#handle(eachport, eachfile)
		print('Parent process %s.' % os.getpid())
		p.apply_async(connect, args=('127.0.0.1', 'XSPLZ', eachinfo['port'], cmd, eachinfo['passwd'], ))
	print('Waiting for all subprocesses done...')
	p.close()
	p.join()
	 
if __name__ == '__main__':  
	main()  