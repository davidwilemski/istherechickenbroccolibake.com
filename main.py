
import umdh

from tornado import web, ioloop, gen, httpclient, escape
import sys

menu = {}

@gen.engine
def _get_menu():
    global menu
    http_client = httpclient.AsyncHTTPClient()
    result = yield gen.Task(http_client.fetch, umdh.APIURL)
    menu = escape.json_decode(result.body)


class MainHandler(web.RequestHandler):
    @web.asynchronous
    @gen.engine
    def get(self):
        results = umdh.search_menu_for(
            menu, "Chicken Broccoli Bake")['results']
        
        if results:
            self.render("index.html", answer="YES")
            return
        self.render("index.html", answer="NO")
        return


application = web.Application([
    (r"/", MainHandler),
])


if __name__ == "__main__":
    port = 8888
    if len(sys.argv) > 1:
        port = sys.argv[1]
    application.listen(port)
    loop = ioloop.IOLoop.instance()
    loop.add_callback(_get_menu)
    ioloop.PeriodicCallback(_get_menu, 300*6*12*1000).start()
    loop.start()
