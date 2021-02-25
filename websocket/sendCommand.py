#!/usr/bin/env python


import json
import urllib2
import requests
import websocket

def getSessionID():
    s = requests.Session()
    URL = "http://172.17.78.147/login_signalnode/?username=tpohebodifohE3E9:5FB4G1798692D581G4G6D5:5D49"
    UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"
 
    header = {"User-Agent" : UA,
              "Referer": URL
              }
 
    #s.get(URL,headers=header)
 
    postData = { 'u': 'whatbeg',
                 'p': '*****'
                 }
    s.post(URL,
           data = postData,
           headers = header)
    f = s.get(URL,headers=header)
    sessionid = f.cookies.get_dict()['sessionid']
    return sessionid



def sendCmd():
    #dic1 = {"pattern":"172.17.78.6","command":"bash /opt/1.sh"}
    dic1 = {"pattern":"172.17.78.6","command":"asdfasdf"}
    #opener = urllib2.build_opener()
    #opener.addheaders.append(('Cookie','sessionid=rfahjhp66kh13br6zod8omn2hvciweyb'))
    #f = opener.open('http://172.17.78.147/exec_cmd/?role=test1&check_assets=172.17.78.6')
    #print f.read()
    sessionid = getSessionID()
    cmdurl = "ws://172.17.78.147/ws/exec?role=test1"
    ws = websocket.create_connection(cmdurl, cookie='sessionid=%s' % sessionid)
    ws.send(json.dumps(dic1))
    print "sent"

    print 'receive...'
    result = ws.recv()
    print 'receive "%s"' % result

    result = ws.recv()
    print 'receive "%s"' % result

    result = ws.recv()
    print 'receive "%s"' % result

    result = ws.recv()
    print 'receive "%s"' % result

    result = ws.recv().replace('<br />', '\n')
    print '%s' % result

    result = ws.recv()
    print 'receive "%s"' % result
    ws.close()

if __name__ == "__main__":
    sendCmd()                                                                                                  
