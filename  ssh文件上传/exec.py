#!/usr/bin/python 
# -*- coding:UTF-8 -*-

import os
import paramiko

def ssh2(ip, port, username, passwd, cmd):
	try:
		ssh = paramiko.SSHClient()
		ssh.load_system_host_keys()
		#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		#private_key = paramiko.RSAKey.from_private_key_file('./web1.sec', password='c%6Nc5kmSQJ89lA0')
		ssh.connect(ip, int(port), username, passwd)#, key_filename="./web1.sec")#, passwd, timeout=20)
		
		#创建会话
		channel = ssh.invoke_shell()
		channel.settimeout(100)

		#通道执行shell的ssh连接
		buff = ''
		resp = ''
		channel.send('ls' + '\n')
		print channel.recv(9999)
		print channel.recv(9999)
		
		#print channel.recv(9999)
		
		
		for m in cmd:
			print 1
			stdin, stdout, stderr = ssh.exec_command(m)
			#stdin.write("yes")
			out = stdout.readlines()
			#out = stderr.readlines()
			#print out
			print out
			#for o in out:
			#    print o,
			#    print '%s\tOK\n'%(ip)
			#    ssh.close()
		ssh.close()
		return out
	except Exception as e:
		print str(e)


if __name__=='__main__':
	cmd = ['touch 2.txt']
	username = "XSPLZ"
	passwd = "c%6Nc5kmSQJ89lA0"
	ip = '127.0.0.1'
	port = '15170'
	ssh2(ip, port, username, passwd, cmd)