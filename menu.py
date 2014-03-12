
import umdh
from tornado import gen, httpclient, ioloop, escape
import yieldpoints


@gen.coroutine
def get_menu(date=None):
    result = {}

    # fetch documents
    http_client = httpclient.AsyncHTTPClient()
    for key in umdh.dining_halls.iterkeys():
        http_client.fetch(umdh.get_menu_url(key, date), callback=(yield gen.Callback(key)))

    keys = set(umdh.dining_halls.keys())
    # parse for chicken broccoli bake
    while keys:
        key, r = yield yieldpoints.WaitAny(keys)
        meals = umdh.search_menu_for(
                escape.json_decode(r.body), 'Chicken Broccoli Bake')
        if meals:
            result[key] = meals
        keys.remove(key)

    print date, result
    raise gen.Return(result)

if __name__ == '__main__':
    loop = ioloop.IOLoop.instance()
    _get_menu()
    loop.start()
    #stuff
