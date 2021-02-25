from subprocess import Popen
import time


url1 = 'http://172.16.1.21/#/page/flow_diagram'
url2 = 'http://172.16.1.21/#/page/dashboard'
url3 = 'http://172.16.1.19:8001/index.html'
url4 = 'http://172.16.1.21/#/page/report_sys'


Popen("python reflash.pyw %s %s" % (url1,'run_condition'),shell=True)
time.sleep(5)

Popen("python reflash.pyw %s %s" % (url2,'key_data'),shell=True)
time.sleep(5)

Popen("python reflash.pyw %s %s" % (url3,'source_count'),shell=True)
time.sleep(5)

Popen("python reflash.pyw %s %s" % (url4,'source_total'),shell=True)
