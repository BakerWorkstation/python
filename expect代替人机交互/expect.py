#!/usr/local/python
#-*-coding:utf-8-*-
#
import pexpect 
 
ip="10.255.48.53" 
name="root" 
pwd="123///" 
 
#发送命令执行交互 
child=pexpect.spawn('ssh  %s@%s' % ("root",ip)  ) 
# 
child.expect ('password:') 
 
child.sendline(pwd) 
 
child.expect('#') 
 
child.sendline('ifconfig') 
 
#发送命令 
child.sendline("exit") 
 
child.interact() 
 
#关闭pexpect 
child.close() 
