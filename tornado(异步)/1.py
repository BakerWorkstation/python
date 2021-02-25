__author__ = 'BurNing'
# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen
from tornado.concurrent import run_on_executor
# 这个并发库在python3自带 在python2需要安装futures
from concurrent.futures import ThreadPoolExecutor
import time
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)
class SleepHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(2)
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        res = yield  self.sleep()
        self.write("when i sleep %s s" % res)
        self.finish()

    @run_on_executor
    def sleep(self):
        time.sleep(5)
        return 5

class JustNowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("i hope just now see you")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
            (r"/sleep", SleepHandler), (r"/justnow", JustNowHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()