#!/user/bin/python
# -*- encoding: UTF-8 -*-

import sys, os
sys.path.append('/opt/autooption/autooption')
sys.path.append('/opt/autooption')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings
from django.contrib import auth

from django.contrib.auth.models import User, Permission, Group
#from autooption.models import HostList, GroupList


def user_regist(username, passwd):
    #check whether include username or not, eg:abc,ab
    try:
        u = User.objects.create_user(username = username, password = passwd)
    except Exception, e:
        print e
        return False
    return True


if __name__ == '__main__' :
    user_list = []
    #user_list.append({'username':'yanbo','password':'qwer1234'})
    #user_list.append({'username':'piaowenyao','password':'qwer1234'})
    #user_list.append({'username':'songdancheng','password':'qwer1234'})
    user_list.append({'username':'1002','password':'123456'})
    for info in user_list:
        user_regist(info['username'], info['password'])
        
    
