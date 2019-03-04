import tornado.ioloop
import tornado.web
import random
import os

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		url = self.request.uri
		page_id = url[1:]
		generate_page(page_id)
		self.render("test/" + page_id + ".html")


if __name__ -- "__main__":
	app = make_app()
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()