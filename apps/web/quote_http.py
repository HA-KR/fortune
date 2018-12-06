# -*- coding: UTF-8 -*-
import os
import random
from twisted.web import server, resource
from twisted.internet import reactor


class QuoteResource(resource.Resource):
    isLeaf = True
    numberRequests = 0

    def __init__(self, quote=None):
        self.quotes = []
        print("Initing Quotes..")
        with open(os.path.join(os.path.dirname(__file__),"resources/fortunes")) as fo:
            self.quotes  = [q for q in fo.read().split("\n%\n") if len(q.strip()) > 0]
        print("Loaded {} quotes".format(len(self.quotes)))

    def quote(self):
        secure_random = random.SystemRandom()
        q = secure_random.choice(self.quotes) or "An apple a day keeps the doctor away"
        return q

    def render_GET(self, request):
        self.numberRequests += 1
        request.setHeader("content-type", "text/plain")
        msg = "[{}] {}".format(self.numberRequests, self.quote()).encode('utf-8')
        return msg


PORT = 8000
proxy_port = int(os.environ.get('PORT', PORT))
reactor.listenTCP(proxy_port, server.Site(QuoteResource()))
reactor.run()

