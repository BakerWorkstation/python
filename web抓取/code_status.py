#coding=utf-8
 
import requests
 
def getStatusCode(url):
    r = requests.get(url, allow_redirects = False)
    return r.status_code
 
 
print getStatusCode('http://www.oschina.net/')
print getStatusCode('http://www.baidu.com/')
print getStatusCode('http://172.16.1.110/download/2EFEBE1BD80BE442702AEAE55AC37439.E872F977')
