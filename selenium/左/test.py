from subprocess import Popen
import time
import win32api
from ctypes import *
import win32con

url1 = 'http://172.16.1.38/permission/sp/welcome.html'
#url2 = 'http://172.16.1.38/permission/sp/welcome.html'
#url3 = 'http://172.16.1.38/permission/sp/welcome.html'
#url4 = 'http://172.16.1.38/permission/sp/welcome.html'


Popen("python reflash.pyw %s %s" % (url1,'run_condition'),shell=True)
time.sleep(30)
#mouse_left_click(965, 13,0)
#mouse_move(594, 559)
#mouse_left_click(594, 559)
#key_combination(0x7A) #F11

Popen("python reflash.pyw %s %s" % (url1,'key_data'),shell=True)
time.sleep(30)

Popen("python reflash.pyw %s %s" % (url1,'source_count'),shell=True)
time.sleep(30)

Popen("python reflash.pyw %s %s" % (url1,'source_total'),shell=True)

