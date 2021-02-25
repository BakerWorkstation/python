#!/usr/bin/envpython 
#coding=utf-8 
from bottle import route,run,view,static_file 
@route('/download/<filename:path>') 
def download(filename): 
    return    static_file(filename,root='/home/bottle/static',download=True) 
run(host='0.0.0.0',port=8000,debug=True) 
