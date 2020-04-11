import tornado.web
import tornado.ioloop
import os

class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class staticRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


if __name__ == "__main__":

    app = tornado.web.Application([
        (r'/',basicRequestHandler),
        (r'/main',staticRequestHandler)],
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        img_path=os.path.join(os.path.dirname(__file__), "img"),
        debug = True)


    app.listen(8800)
    print("server running in port 8800")
    tornado.ioloop.IOLoop.current().start()
