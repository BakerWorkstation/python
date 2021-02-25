#!/usr/bin/python
# -*- encoding: utf-8 -*-

#-------------------------------------------------------------
#  __author__ : Sylar
#       Timer : 2016/09/08
#    function : calculate file  md5 and crc32
#-------------------------------------------------------------

  
import time
import hashlib
import os
import sys
import binascii

def get_crc32(file): 
    """ 
      Generates the crc32 hash of the v. 
      @return: str, the str value for the crc32 of the v 
    """
    ff = open(file, 'r')
    sum = ''
    for i in  ff.readlines():
        sum += i
    ff.close() 
    return '%X' % (binascii.crc32(sum) & 0xffffffff)
  
def get_hexdigest(filename):
    hashobj = hashlib.md5()
    with open(filename, 'rb') as f:        
        hashobj.update(f.read())
    md5_str = hashobj.hexdigest().upper()
  
    return md5_str


if __name__ == "__main__":
    try:
        file = sys.argv[1]
    except:
        print '''
        \033[31mWarning : command not right!\033[0m

        \033[32m(HELP)
              parameter 1 :  filepath

              For example :  " python  calculate_md5_crc32.py  /etc/rc.local "\033[0m
              '''
        os._exit(0)
    print 'md5   : %s' % get_hexdigest(file)
    print 'crc32 : %s' % get_crc32(file)
