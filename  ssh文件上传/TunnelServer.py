#!/usr/bin/python

import os
import time
import paramiko
from sshtunnel import SSHTunnelForwarder


server = SSHTunnelForwarder(
                            ssh_address_or_host=('47.75.66.217', 60022),
                            ssh_username="13504845624",
                            ssh_password="Baker@231",
                            #ssh_pkey="/var/ssh/rsa_key",
                            #ssh_private_key_password="secret",
                            remote_bind_addresses=[
                                                   ('10.10.10.80', 15170),    
                                                   ('10.10.10.77', 15170),
                                                   ('10.10.10.78', 15170),
                                                   ('10.10.10.74', 15170),
                                                   ('10.10.10.70', 15170),
                                                   ('10.10.10.69', 15170),
                                                   ('10.10.10.92', 15170)],

                            local_bind_addresses=[
                                                   ('127.0.0.1', 15170),   #  api1
                                                   ('127.0.0.1', 15171),   #  api2
                                                   ('127.0.0.1', 15172),   #  task1
                                                   ('127.0.0.1', 15173),   #  task2
                                                   ('0.0.0.0', 15174),   #  web1
                                                   ('127.0.0.1', 15175),   #  web2
                                                   ('127.0.0.1', 15176)]   #  web3
)
server.start()
print 'start listen ...'
#while 1:
#	pass

#client = paramiko.SSHClient()

#client.load_system_host_keys()
#client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#private_key = paramiko.RSAKey.from_private_key_file('./web1.sec', password='c%6Nc5kmSQJ89lA0')
	
#client.connect(hostname='127.0.0.1', port=15170, username='XSPLZ')# password='c%6Nc5kmSQJ89lA0', pkey=private_key)#, allow_agent=False, 

#print('FINISH!')