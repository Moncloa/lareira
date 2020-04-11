import tornado.web
import tornado.ioloop


class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World!")

class staticRequestHandler(tornado.web.RequestHandler):
    def get(self):
        video_url = "192.168.0.111:8080/video_feed"
        self.render("templates/index.html")


if __name__ == "__main__":
    app = tornado.web.Application([
        (r'/',basicRequestHandler),
        (r'/index.html',staticRequestHandler)




    ])

    app.listen(8800)
    tornado.ioloop.IOLoop.current().start()
    print("server running in port 8800")