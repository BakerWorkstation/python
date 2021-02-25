# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import hashlib
import os.path
from socket import *
from os import _exit
import json
import base64



class MainHandler(tornado.web.RequestHandler):
	def get(self,path):
		#self.write("hello world!")
		#self.set_header('Content-Transfer-Encoding', 'binary')
                #path = '/dev/shm/'+path
		print '< filename : %s >' % path
                #if path.startswith("/download/") == False:
                #        raise tornado.web.HTTPError(403)
                        #return

                #f = open(path, 'rb')
		md5 = hashlib.md5()
                #while True:
                #        p = f.read(4096)
                #        if not p:
                #            break
                #        md5.update(p)
                #f.close()
		self.set_header('md5', md5.hexdigest().upper())
		self.set_header('Content-Disposition', 'attachment; filename="%s"' %  path)#os.path.basename(path))
		self.set_header('Content-Transfer-Encoding', 'binary')

		testdict={ "filename" : path  , "filedata" : "" , "index" : "download"}
		tcpCliSock = socket(AF_UNIX, SOCK_STREAM)
		server_address = '/dev/shm/ipc.fd'
		try:
			tcpCliSock.connect(server_address)
		except error,e:
			print '>>> test : ',str(e), '服务端没启动'
			_exit(0)
		send = json.dumps(testdict)
		#print send
		tcpCliSock.send(send)
		sum = ''
		while True:
			receive = tcpCliSock.recv(26000)
			sum = sum + receive
			if receive[-1] == '}':
				receive = sum
				break
		receive = json.loads(receive)
		receive = base64.b64decode(receive['body'])
		print '< filesize : %s KB >' % int(round(float(len(receive))/1024))
		#receive = receive.encode(encoding = 'gbk')
		#print len(receive['body'])
		self.set_header('Content-Type', 'application/octet-stream')
		#receive = receive.replace('\n','<br>')
		#print receive
		self.set_header('Content-Length', '%d' % len(receive))
		self.write(receive)
		status = tcpCliSock.recv(16000)
		print '< status : %s >' % status
		print ' connection close '
		#	break
		tcpCliSock.close()

settings = {
	"debug": True,
	#"static_path": "/dev/shm/",
	#"static_path": os.path.join(os.path.dirname(__file__), "download"),
	"cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
}

application = tornado.web.Application([
	(r"/download/(.*)", MainHandler),
	#(r"/download/?", MainHandler),
], **settings)

if __name__ == "__main__":
	application.listen(8000)
	tornado.ioloop.IOLoop.instance().start()
