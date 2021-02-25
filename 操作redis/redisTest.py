#!/usr/bin/env python
# -*- coding:utf-8 -*-
  
import redis  
  
class CRedis:  
  
    def __init__(self):  
        self.host = '127.0.0.1'
        self.port = 6379
        self.db = 0  
        self.password = ''
        self.r = redis.StrictRedis(host=self.host, port=self.port, db=self.db, password=self.password)  
   
    #1. strings 类型及操作  
    #设置 key 对应的值为 string 类型的 value  
    def set(self, key, value):  
        return self.r.set(key, value)  
      
    def get(self, key):  
        return self.r.get(key)  
  
    #设置 key 对应的值为 string 类型的 value。如果 key 已经存在,返回 0,nx 是 not exist 的意思  
    def setnx(self, key, value):  
        return self.r.setnx(key, value)  
   
    #设置 key 对应的值为 string 类型的 value,并指定此键值对应的有效期  
    def setex(self, key, time, value):  
        return self.r.setex(key, time, value)  
   
    #设置指定 key 的 value 值的子字符串  
    #例：setrange name 8 gmail.com  
    #其中的 8 是指从下标为 8(包含 8)的字符开始替换  
    def setrange(self, key, num, value):  
        return self.r.setrange(key, num, value)  
   
    #获取指定 key 的 value 值的子字符串  
    def getrange(self, key, start ,end):  
        return self.r.getrange(key, start, end)  
    #删除  
    def remove(self, key):  
        return self.r.delete(key)  
   
    #自增  
    def incr(self, key, default = 1):  
        if (1 == default):  
            return self.r.incr(key)  
        else:  
            return self.r.incr(key, default)  
   
    #自减  
    def decr(self, key, default = 1):  
        if (1 == default):  
            return self.r.decr(key)  
        else:  
            return self.r.decr(key, default)  
              
    #清空当前db  
    def clear(self):  
        return self.r.flushdb()  
          
if __name__ == '__main__':  
    r = CRedis()  
    print r.get('test')  
    #r.remove('test')  
