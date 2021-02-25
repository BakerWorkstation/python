# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import define, options
import json
from tornado.escape import json_decode

define("port",default=8888,help='run a test')
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        info={'user':'leno'}
        jinfo=json.dumps(info)
        self.write(jinfo)

    def post(self,*args,**kwargs):
        print 'post message'
        print self.request.remote_ip
        print self.request.body_arguments
        data = json_decode(self.request.body)
        #user = data['user']
        #pw = data['passwd']
        #print user,pw
        print data
        #data=json.loads(user)
        #print jdata
        #data=json.loads(jdata)

    def set_default_headers(self):
        self.set_header('Content-type','application/json;charset=utf-8')

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
