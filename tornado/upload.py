#-*-coding:utf8-*-
import tornado.ioloop
import tornado.web

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
        file_dict_list = self.request.files['file']
        for file_dict in file_dict_list:
            filename = file_dict["filename"]
            #f = open("/data/web/upload/%s" % filename, "wb")
            f = open("/dev/shm/%s" % filename, "wb")
            print file_dict["body"]
            f.write(file_dict["body"])
            f.close()
       
            #self.write("<a href='/upload'>asdf</a>")
            self.redirect('/upload')
application = tornado.web.Application([
    (r"/upload/?", UploadFileHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
