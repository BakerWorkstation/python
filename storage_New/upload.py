# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
from socket import *
import json
from os import _exit
import base64
import time
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')


class UploadFileHandler(tornado.web.RequestHandler):
    def get(self):
	self.write('''
	    <!doctype html>
              <html>
                <head>
                   <meta charset="utf-8" />
                   <title>文件上传</title>
                </head>
                <body>
                   <form action="/upload/" enctype="multipart/form-data" method="post">
                   <input name="file" type="file">
                   <input type="submit" value="Submit">
                   </form>
                </body>
              </html>''')
    def post(self):
        #self.write('upload successfully !')
        file_dict_list = self.request.files['file']
        BUFSIZ = 16000
        tcpCliSock = socket(AF_UNIX, SOCK_STREAM)
        server_address = '/dev/shm/ipc.fd'

        try:
            tcpCliSock.connect(server_address)
            #tcpCliSock.setblocking(0)
        except error,e:
            print '>>> test : ',str(e), '服务端没启动'
            _exit(0)

        for file_dict in file_dict_list:
            filename = file_dict["filename"]
            filedata = file_dict["body"]
            print '< filename : %s >'  % filename
            print '< filesize : %s KB > ' % int(round(float(len(filedata))/1024))
            filedata = base64.b64encode(filedata)
            testdict = {"filename" : filename , "filedata" : filedata , "index" : "upload"}
            #print testdict
            text = json.dumps(testdict)
            tcpCliSock.sendall(text)
            #print '>>> send finish!'
            receive = tcpCliSock.recv(16000)
            print '< status   : %s >' % receive
        tcpCliSock.close()
        print ' connection  close '
        #self.write("<a href='/upload'>asdf</a>")
        #self.redirect('/upload')

application = tornado.web.Application([
    (r"/upload/?", UploadFileHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
