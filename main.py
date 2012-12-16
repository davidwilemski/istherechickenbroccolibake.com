
import umdh

from tornado import web, ioloop, gen, httpclient, escape
import tornado.options
from xml.etree import ElementTree as ET
import yieldpoints

import sys


menu = []

@gen.engine
def _cache_menu():
    global menu
    menu = []
    menu = yield gen.Task(_get_menu)


@gen.engine
def _get_menu(callback):
    result = []

    # fetch documents
    http_client = httpclient.AsyncHTTPClient()
    for key, url in umdh.dining_halls.iteritems():
        http_client.fetch(url, callback=(yield gen.Callback(key)))

    keys = set(umdh.dining_halls.keys())
    # parse for chicken broccoli bake
    while keys:
        key, r = yield yieldpoints.WaitAny(keys)
        if umdh.search_menu_for(
                ET.fromstring(r.body), 'Chicken Broccoli Bake'):
            result.append(key)
        keys.remove(key)

    print result
    callback(result)


class MainHandler(web.RequestHandler):
    @web.asynchronous
    @gen.engine
    def get(self):
        global menu
        if menu:
            self.render("index.html", answer="YES")
            return
        self.render("index.html", answer="NO")
        return


application = web.Application([
    (r".*", MainHandler),
])


if __name__ == "__main__":
    tornado.options.parse_command_line()
    port = 9999
    if len(sys.argv) > 1:
        port = sys.argv[1]
    application.listen(port)
    loop = ioloop.IOLoop.instance()
    loop.add_callback(_cache_menu)
    ioloop.PeriodicCallback(_cache_menu, 60*60*2*1000).start()
    loop.start()
