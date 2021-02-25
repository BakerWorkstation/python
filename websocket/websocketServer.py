#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import os
import json
import time
import fcntl
import random
import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.httpserver
from tornado import gen
from concurrent.futures import ThreadPoolExecutor

thread_pool = ThreadPoolExecutor(100)

iepQueue = {}
ptdQueue = {}
ptdHandlerQueue = {}


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    webSocketlist = {}
    classify = None
    hardwareId = None
    r= None

    # @gen.coroutine
    # def on_open_coroutine(self, message):
    #     #self.write_message('Message:', message)
    #
    #     def worker_A(websocket, x):
    #         time.sleep(1)
    #         print('TICK', x)
    #         pass
    #         return x
    #
    #     print('scheduling and yielding')
    #     #for x in range(0, 30):
    #     #    test = yield thread_pool.submit(worker_A, self, x)
    #         #self.write_message(json.dumps(test))
    #
    #     print('done yielding')

    def check_origin(self, origin):
        return True

    @gen.coroutine
    def on_open_coroutine(self, classify, hardwareId):
        def worker(self, classify, hardwareId):
            self.classify = classify
            self.hardwareId = hardwareId
            url = self.request.uri
            print ('新连接接入中:')
            print('分类: %s' % self.classify)
            print('设备ID: %s' % self.hardwareId)
            try:
                if classify == 'ptd':
                    print(self)
                    # 更新PTD设备连接数队列
                    try:
                        if self.hardwareId in ptdQueue:
                            ptdQueue[self.hardwareId] += 1
                        else:
                            ptdQueue[self.hardwareId] = 1
                    except Exception:
                        ptdQueue[self.hardwareId] = 1

                    # 更新PTD设备连接句柄队列
                    if self.hardwareId in ptdHandlerQueue:
                        ptdHandlerQueue[self.hardwareId].add(self)
                    else:
                        ptdHandlerQueue[self.hardwareId] = set([self])

                elif classify == 'iep':
                    print(self)
                    # 更新IEP设备连接数队列
                    try:
                        if self.hardwareId in iepQueue:
                            iepQueue[self.hardwareId] += 1
                        else:
                            iepQueue[self.hardwareId] = 1
                    except Exception:
                        iepQueue[self.hardwareId] = 1

            except Exception as e:
                print(str(e))
                pass

        yield thread_pool.submit(worker, self, classify, hardwareId)

    def open(self, classify, hardwareId):
        self.classify = classify
        self.hardwareId = hardwareId
        url = self.request.uri
        print('新连接接入中:')
        print('分类: %s' % self.classify)
        print('设备ID: %s' % self.hardwareId)
        try:
            if classify == 'ptd':
                print(self)
                # 更新PTD设备连接数队列
                try:
                    if self.hardwareId in ptdQueue:
                        ptdQueue[self.hardwareId] += 1
                    else:
                        ptdQueue[self.hardwareId] = 1
                except Exception:
                    ptdQueue[self.hardwareId] = 1

                # 更新PTD设备连接句柄队列
                if self.hardwareId in ptdHandlerQueue:
                    ptdHandlerQueue[self.hardwareId].add(self)
                else:
                    ptdHandlerQueue[self.hardwareId] = set([self])

            elif classify == 'iep':
                print(self)
                # 更新IEP设备连接数队列
                try:
                    if self.hardwareId in iepQueue:
                        iepQueue[self.hardwareId] += 1
                    else:
                        iepQueue[self.hardwareId] = 1
                except Exception:
                    iepQueue[self.hardwareId] = 1

        except Exception as e:
            print(str(e))
            pass
        #tornado.ioloop.IOLoop.current().spawn_callback(self.on_open_coroutine, classify, hardwareId)

    def on_message(self, message):
        try:
            #print ("get message:" , message)
            #self.write_message(message)
            print('receive')
            #self.r.write(message)
            #self.r.finish()
        except WebSocketClosedError as e:
            print (e)

    @classmethod
    def get_one_conn(cls,uuid,target,r):
        target = '/' + target
        if uuid in ptdHandlerQueue:
            one_conn = random.choice(list(ptdHandlerQueue[uuid]))
            print(list(ptdHandlerQueue[uuid]))
            print(one_conn)
            one_conn.r = r
            request =  r.request
            print(target)
            #print(request)
            #print(dir(request))
            url = "/api/ids/data/download"
            #requestBody = '''%s %s %s\r\n%sContent-Length: 51\r\n\r\n{"star":1572578271,"rid":39686,"sign":[2164260954]}''' % ('POST', url, request.version, request.headers)
            #print(requestBody)
            #print(requestBody)
            #print()
            #print("""GET /api/summary/current HTTP/1.0\r\nHost: 127.0.0.2\r\nUser-Agent: curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.45.0 OpenSSL/1.0.1e zlib/1.2.3 libidn/1.18 librtmp/2.3\r\nAccept: */*\r\nContent-Length: 0\r\n\r\n""")
            #test_str = bytes("""GET /api/summary/current HTTP/1.0\r\nHost: 127.0.0.2\r\nUser-Agent: curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.45.0 OpenSSL/1.0.1e zlib/1.2.3 libidn/1.18 librtmp/2.3\r\nAccept: */*\r\nContent-Length: 0\r\n\r\n""","utf-8")
            requestBody = """POST /api/ids/data/download HTTP/1.0\r\nHost: 10.255.175.98\r\nContent-Type: text/plain\r\nUser-Agent: PostmanRuntime/7.19.0\r\nAccept: */*\r\nCache-Control: no-cache\r\nPostman-Token: f520bc78-f414-4b2b-8166-fc4a4354b623,49244893-325d-4071-8141-7c401e36d476\r\nContent-Length: 51\r\n\r\n{"star":1572578271,"rid":39686,"sign":[2164260954]}"""
            print(requestBody)
            test_str = bytes(requestBody, "utf-8")
            one_conn.write_message(test_str)
            print('send finish')
            #one_conn.close()
        else:
            r.finish()

    def on_close(self):
        classify = self.classify
        hardwareId = self.hardwareId
        #url = self.request.uri
        print ('连接关闭')
        print('*' * 50)
        try:
            if classify == 'ptd':
                if hardwareId in ptdQueue:
                    ptdQueue[hardwareId] -= 1
                    if ptdQueue[hardwareId] == 0:
                        ptdQueue.pop(hardwareId)
            elif classify == 'iep':
                if hardwareId in iepQueue:
                    iepQueue[hardwareId] -= 1
                    if iepQueue[hardwareId] == 0:
                        iepQueue.pop(hardwareId)
        except:
            pass


class ListPTDHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(ptdQueue))

class ListIEPHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(iepQueue))

class RemotePTDAccessMGMTHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self,uuid,target):
        if uuid in ptdHandlerQueue:
            #self.set_header('Content-Disposition', "attachment;filename=1.pcap;charset=utf8")
            WebSocketHandler.get_one_conn(uuid,target,self)
        else:
            self.finish()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r'/api/v1/device/(?P<classify>\w*)/remote_access/(?P<hardwareId>\w*)', WebSocketHandler),
        (r'/api/internal/remote_access/device/ptd/list', ListPTDHandler),
        (r'/api/internal/remote_access/device/iep/list', ListIEPHandler),
        (r'/api/internal/remote_access/device/ptd/data/(?P<uuid>\w*)/(?P<target>.*)', RemotePTDAccessMGMTHandler)
        ]

        settings = {"template_path": ".", 'debug' : False, "websocket_ping_interval": 10}
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app,
                                           ssl_options={
                                               "certfile": os.path.join(os.path.abspath("."), "server.crt"),
                                               "keyfile": os.path.join(os.path.abspath("."), "server.key")}
                                           )
    # 单进程
    server.listen(4500)
    tornado.ioloop.IOLoop.instance().start()

    # 多进程
    # server.bind(4499)
    # server.start(num_processes=16)
    # tornado.ioloop.IOLoop.instance().start()
