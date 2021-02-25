from subprocess import Popen
import time

url1 = 'http://172.16.1.38/permission/sp/login.html'
#url2 = 'http://172.16.1.38/permission/sp/login.html'
#url3 = 'http://172.16.1.29:8042/'
url4 = 'http://172.16.1.38/permission/sp/login.html'



#Popen("python reflash.pyw %s %s" % (url1,'data_pandect'),shell=True)
#time.sleep(30)

#Popen("python reflash.pyw %s %s" % (url2,'key_data'),shell=True)
#time.sleep(30)

#Popen("python reflash.pyw %s %s" % (url3,'whole_view'),shell=True)
#time.sleep(30)

Popen("python reflash.pyw %s %s" % (url4,'probe'),shell=True)
