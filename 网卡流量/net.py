'''
@Author: your name
@Date: 2020-05-26 11:17:39
@LastEditTime: 2020-05-26 13:32:17
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /opt/net/1.py
'''
#!/usr/bin/env Python
import time
import sys

if len(sys.argv) > 1:
	INTERFACE = sys.argv[1]
else:
	INTERFACE = 'eth0'
STATS = []
print('Interface:',INTERFACE)

def	rx():
	ifstat = open('/proc/1/net/dev').readlines()
	for interface in  ifstat:
		if INTERFACE in interface:
			stat = float(interface.split()[1])
			STATS[0:] = [stat]

def	tx():
	ifstat = open('/proc/1/net/dev').readlines()
	for interface in  ifstat:
		if INTERFACE in interface:
			stat = float(interface.split()[9])
			STATS[1:] = [stat]

print('In			Out')
rx()
tx()

while	True:
	time.sleep(1)
	rxstat_o = list(STATS)
	rx()
	tx()
	RX = float(STATS[0])
	RX_O = rxstat_o[0]
	TX = float(STATS[1])
	TX_O = rxstat_o[1]
	RX_RATE = round((RX - RX_O)/1024/1024,3)
	TX_RATE = round((TX - TX_O)/1024/1024,3)
	print(RX_RATE ,'MB		',   TX_RATE ,'MB')