#  -*- coding:utf-8 -*-
import urllib
import urllib2
import json

url='http://127.0.0.1:8888'
values ={'user':'c','passwd':'d'}
jdata = json.dumps(values)
req = urllib2.Request(url)
req.add_data(jdata)
print req.headers
response = urllib2.urlopen(req)
