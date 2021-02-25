#!/usr/bin/python  
# encoding:utf-8

import paramiko 
import time
import re  
  
  
class SecConnect:  
	def __init__(self):  
		self.ssh = paramiko.SSHClient()  
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
		bip = '47.75.66.217'  
		buser = '13504845624'  
		bpasswd = 'Baker@231'  
  
		#sip = '10.10.10.70'
		sip = '47.75.60.6'
		suser = 'XSPLZ'  
		spasswd = 'c%6Nc5kmSQJ89lA0'  
  
		port = 15170  
		passinfo = "\'s password: "  # 返回要求输入密码的提示字串  
		  
		# 连接堡垒机  
		self.ssh.connect(bip, 60022, buser, bpasswd)
		#print 1
		private_key = paramiko.RSAKey.from_private_key_file('/Users/songdancheng/凯撒私钥/web1.sec', password=spasswd)
		#self.ssh.connect(hostname=sip, port=port, username=suser,  pkey=private_key)
		self.channel = self.ssh.invoke_shell()  
		self.channel.settimeout(10)  
		print 2
		
		#print  self.channel.recv(9999)
		#print  self.channel.recv(9999)
		
		# 连接目标主机
		#print self.channel.send('ssh -p 15170 10.10.10.70' + '\n')
		print self.channel.send('ssh -p 15170 XSPLZ@47.75.60.6' + '\n\n')
		#self.repeat = 0  # 要区分是否为第一次调用命令,第一次与后续调用格式不同
  
        # ---------------------------------------------------
		buff = ''  
		resp = ''  

		print  self.channel.recv(29999)
		print  self.channel.recv(29999)
		#print  self.channel.recv(9999)
		self.channel.send('hostname' + '\n')
		print  self.channel.recv(9999)
		print  self.channel.recv(9999)
		print  self.channel.recv(9999)
		# ---------------------------------------------------
		
		#print  self.channel.recv(9999)
		#print  self.channel.recv(9999)
		
		#print 4
		#while not buff.endswith(passinfo):  
		#	try:  
		#		resp = self.channel.recv(9999)
		#		print resp 
		#	except Exception as e:  
		#		print e  
		#	buff += resp  
		#	if not buff.find('yes/no') == -1:  
		#		print "ok"  
		#		self.channel.send('yes\n')  
		#		buff = ''  
		#self.channel.send('ZGdtFCOiSK#5Dkf4' + '\n') 

		#print  self.channel.recv(9999)
		#print  self.channel.recv(9999)
		#print  self.channel.recv(9999)
		#print 5
		#self.channel.send('ifconfig' + '\n')
		#print  self.channel.recv(9999)
		#print 6
		#print  self.channel.recv(9999)
		  
	# 若需要，输入sudo的权限及密码，缺省为用户权限     
	def do_commend(self, commend, permission='user', passwd=''):  
		"""执行命令，返回显示结果"""  
		# 以数据包的形式接受目标主机返回的信息  
		if permission == 'sudo':  
			commend = 'sudo ' + commend + '\n'  
			self.channel.send(commend)  
			buff = ''  
			try:  
				while buff.find('# ') == -1:  
					resp = self.channel.recv(9999)  
					buff += resp  
			except Exception, e:  
				print e  
			# print buff  
			self.channel.send(passwd + '\n')  
		else:  
			commend += '\n'  
			self.channel.send(commend)  
		buff = ''  
		recall = ''  
		try:  
			while buff.find('# ') == -1:  
				resp = self.channel.recv(9999)  
				buff += resp  
		except Exception, e:  
			print e  
		# print buff  
		  
		# 正则表达式提取出需要的回执信息  
		start = 0  
		finish = 0  
		if self.repeat == 0:    # 第一次调用命令  
			# print "fir"  
			flag1 = 0  
			flag2 = 0  
			for i in range(len(buff)):  
				if buff[i] == '$':  
					flag1 += 1  
					continue  
				elif flag1 == 1 and flag2 == 0:  
					if buff[i] == '\n':  
						start = i + 1  
						flag2 = 1  
						continue  
				elif flag1 == 1 and flag2 == 1:  
					if buff[i] == '\n':  
						finish = i - 1  
						self.repeat = 1  
		elif self.repeat == 1:  
			lines = 1  
			flag = 0  
			for i in range(len(buff)):  
				if buff[i] == '\n' and lines > 0:  
					lines -= 1  
					start = i+1  
				elif lines == 0:  
					flag = 1  
				if flag == 1 and buff[i] == '\n':  
					finish = i-1  
		# print start, finish  
		tip = start  
		for i in range(finish - start + 1):  
			recall += buff[tip]  
			tip += 1  
		# print recall  
		return recall  
  
	def close(self):  
		"""关闭全部连接（堡垒机和二级主机）"""  
		self.channel.close()  
		self.ssh.close()
		
if __name__ == '__main__':
	S = SecConnect()
	S.close()