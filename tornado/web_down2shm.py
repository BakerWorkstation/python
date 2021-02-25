#!/usr/bin/python
import tornado.ioloop
import tornado.web
import hashlib
import os.path

class MainHandler(tornado.web.RequestHandler):
	def get(self,path):
		#self.write("hello world!")
		#self.set_header('Content-Transfer-Encoding', 'binary')
                path = '/dev/shm/'+path
                print path
                #if path.startswith("/download/") == False:
                #        raise tornado.web.HTTPError(403)
                        #return

       	        if os.path.isfile(path):
                        self.set_header('Content-Type', 'application/octet-stream')
                        self.set_header('Content-Length', os.path.getsize(path))
                        f = open(path, 'rb')
                        md5 = hashlib.md5()
                        while True:
                                p = f.read(4096)
                                if not p:
                                    break
                                md5.update(p)
                        f.close()
                        self.set_header('md5', md5.hexdigest().upper())
		        self.set_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(path))
                        self.set_header('Content-Transfer-Encoding', 'binary')
		        f = open(path, 'rb')
		        while True:
                                p = f.read(4096)
		                if not p:
                		    break
		                self.write(p)
		        f.close()


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
