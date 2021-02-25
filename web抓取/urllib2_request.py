# -*- coding: utf-8 -*-
# env: python2.7

import urllib2
from urllib import urlencode
from cookielib import LWPCookieJar
from time import strftime, sleep
from getpass import getpass
from re import compile

class curl:

    def __init__(self):
        self.logindata = {}
        self.username = ''
        self.password = ''
        self.randcode = ''
        #self.ifneedrefreshrandcode = False   #重复登录时是否需要重新输入验证码

        #在http交互中即时更新cookie
        self.cookiejar = LWPCookieJar()
        cookiesupport = urllib2.HTTPCookieProcessor(self.cookiejar)
        opener = urllib2.build_opener(cookiesupport, urllib2.HTTPHandler)
        urllib2.install_opener(opener)



    #登录动作
    def login(self, loginrand = ''):
        #self.logindata['loginRand'] = loginrand                 #随机码
        self.logindata['loginUser.user_name'] = self.username   #用户名
        self.logindata['nameErrorFocus'] = ''
        self.logindata['user.password'] = self.password         #用户密码
        self.logindata['passwordErrorFocus'] = ''

        try:
            req = urllib2.Request('https://www.virustotal.com/intelligence/search/?query=engines%3A%22CVE-2010-2569%22', urlencode(self.logindata))
            data = urllib2.urlopen(req)
            text = data.read().decode(encoding='utf-8').encode(encoding='gb2312') #将utf-8解码再编码为gb2312
            print text
            return text
        except:
            pass


def main():

    while ch.username == '':
        ch.username = '47385024@163.com'
    while len(ch.password) < 6:
        #print '\r密码：',
        ch.password = '7788945a'
    #print '\r'

    
    print '登陆中...'
    text = ch.login()
    print text

if __name__ == '__main__':
    ch = curl()
    main()
