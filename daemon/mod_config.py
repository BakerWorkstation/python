#!/usr/bin/env python
#encoding:utf-8
#name:mod_config.py

import ConfigParser
import os

#获取config配置文件
class ParseConfig(object):

    def __init__(self, path):
        self.config = ConfigParser.ConfigParser()
        self.config.read(path)
   
    def getsection(self):
        return self.config.sections()
 
    def getconfig(self, section):
        return (
                self.config.get(section, 'enabled'),
                self.config.get(section, 'command'))
        
    def getcommand(self, section):
        return self.config.get(section, 'command')
