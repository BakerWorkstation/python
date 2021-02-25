#!/usr/bin/env python

import httplib
import base64

#userAgent = "Mozilla/5.0 (Windows NT 5.1; rv:26.0) Gecko/20100101 Firefox/26.0"
auth = base64.b64encode('%s:%s' % ('tomcat', 'tomcat')).replace('\n', '')

h = httplib.HTTPConnection('192.168.153.128', 8080)
h.putrequest('GET', '/manager/status')
#h.putheader('Host', '192.168.153.128:8080')
#h.putheader('User-agent', userAgent)
#h.putheader('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
#h.putheader('Accept-Language','en-us')
h.putheader('Accept-Encoding','gzip, deflate')

h.putheader('Authorization', 'Basic %s' % auth)
h.endheaders()

print dir(h)
#statuscode, statusmessage, headers = h.getreply()
data = h.getresponse()
print dir(data)
print data.read()

