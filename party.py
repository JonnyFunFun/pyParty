#!/usr/bin/env python

try:
    import tornado.httpserver
    import tornado.ioloop
    import tornado.wsgi
except ImportError:
    print(">> I need tornado installed to do this.\n>> Please run 'pip install tornado' to do this.\n")
    raise

import django.core.handlers.wsgi
import os
from optparse import OptionParser

def run_tornado_party(port=80, address="0.0.0.0"):
    os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'
    application = django.core.handlers.wsgi.WSGIHandler()
    container = tornado.wsgi.WSGIContainer(application)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(port, address)
    print "Running Tornado pyParty at http://%s:%s/..." % (address, port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
    print "\nThanks for partying with us..."

if __name__ == "__main__":
    # defaults
    parser = OptionParser(usage="usage: %prog [-p port] [-b binding]")
    parser.add_option("-p", "--port", dest="port", action="store", type="int", help="port to listen on (default: 80)")
    parser.add_option("-b", "--bind", dest="addr", action="store", type="string", help="address to bind to (default: 0.0.0.0)")
    (options, args) = parser.parse_args()
    run_tornado_party(port=options.port or 80,address=options.addr or "0.0.0.0")