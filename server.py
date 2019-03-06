import tornado.ioloop
import tornado.web
import random
import os

from domato.generator import generate_samples

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		generator_dir = os.path.dirname(__file__) + 'domato'
		print("dir:"+generator_dir)
		url = self.request.uri
		page_id = url[6:]
		# page = generate_page()
		page_path = 'test/' + str(page_id) + '.html'
		generate_samples(generator_dir, [page_path])
		# with open(page_path, "wb") as f:
			# f.write(page)
		# print(self.request.uri)
		# print(self.request.uri[1:])
		self.render(page_path)

def make_app():
    return tornado.web.Application([
        (r"/fuzz", MainHandler),
    ])

if __name__ == "__main__":
	app = make_app()
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()