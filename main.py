
import umdh

from tornado import web, ioloop, gen, httpclient, escape
import tornado.options
import yieldpoints
import dateutil.relativedelta

import datetime
import os
import sys

import menu


_menu = {}
_menu_next = {}
_menu_next_date = None

@gen.coroutine
def _cache_menu():
    global _menu
    global _menu_next
    global _menu_next_date
    _menu = yield menu.get_menu()

    _menu_next_date = datetime.date.today()
    while not _menu_next:
        # short circuit if greater than 30 days
        if _menu_next_date > datetime.date.today() + dateutil.relativedelta.relativedelta(days=30):
            _menu_next_date = None
            _menu_next = {}
            return

        _menu_next_date += dateutil.relativedelta.relativedelta(days=1)
        _menu_next = yield menu.get_menu(_menu_next_date)


class MainHandler(web.RequestHandler):
    @web.asynchronous
    @gen.engine
    def get(self):
        global _menu
        global _menu_next_date
        if _menu:
            self.render("index.html", answer="YES", locations=_menu)
            return
        self.render("index.html", answer="NO", locations=_menu, future_date=_menu_next_date)
        return


application = web.Application([
    (r".*", MainHandler),
])


if __name__ == "__main__":
    tornado.options.parse_command_line()
    port = os.environ.get('PORT', 9999):

    application.listen(port, xheaders=True)
    loop = ioloop.IOLoop.current()
    loop.add_callback(_cache_menu)
    ioloop.PeriodicCallback(_cache_menu, 60*60*2*1000).start()
    loop.start()
