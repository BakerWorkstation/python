#!/usr/bin/env python

import paramiko

hostname='172.17.78.6'

port=22

username='new'

pkey='./id_rsa'

key=paramiko.RSAKey.from_private_key_file(pkey)

s=paramiko.SSHClient()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

s.load_system_host_keys()

s.connect(hostname,port,username,pkey=key)

stdin,stdout,stderr=s.exec_command('pwd')

print stdout.read().strip()
