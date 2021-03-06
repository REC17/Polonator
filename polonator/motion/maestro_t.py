#!/usr/bin/env python
# encoding: utf-8
"""
maestro_t.py

Created by Nick Conway on 2011-01-04.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import os

# This is the Twisted Maestro client

import sys

from twisted.internet import defer
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.protocols.basic import NetstringReceiver
from twisted.conch.telnet import TelnetTransport, TelnetProtocol


host = '10.0.0.56'
port = 23

class MaestroClientProtocol(TelnetProtocol):
    def connectionMade(self):
        print "connected\n!"
        self.sendRequest(self.factory.message)
    # end def
    
    def sendRequest(self, message):
        self.transport.write(message)
    # end def
    
    def dataReceived(self, data):
        #if data == '>':
        self.transport.loseConnection()
        self.messageReceived(data)
        # end if
    # end def
    
    def messageReceived(self, message):
        self.factory.handleMessage(message)
    # end def
# end class

class MaestroClientFactory(ClientFactory):

    protocol = MaestroClientProtocol

    def __init__(self, message):
        self.message = message
        self.deferred = defer.Deferred()
    # end def
    
    def buildProtocol(self, addr):
        return TelnetTransport(MaestroClientProtocol)
    
    def handleMessage(self, message):
        d, self.deferred = self.deferred, None
        d.callback(message)
    # end def
    
    def clientConnectionLost(self, _, reason):
        if self.deferred is not None:
            d, self.deferred = self.deferred, None
            d.errback(reason)
    # end def
    
    clientConnectionFailed = clientConnectionLost
# end class

class MaestroProxy(object):
    """
    I proxy requests to the maestro service.
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
    # end def
    
    def xmit(self, message):
        factory = MaestroClientFactory(message)
        from twisted.internet import reactor
        reactor.connectTCP(self.host, self.port, factory)
        return factory.deferred
    # end def
# end class

def maestro_main():
    global host, port
    proxy = MaestroProxy(host,port)

    from twisted.internet import reactor

    #message = "some maestro thing"
    filter_number = 0 # cy3
    #filter_number = 3 # cy5
    message =  "Theta.xq##gotofilter(%d);\n\r" % filter_number
    @defer.inlineCallbacks
    def send_maestro_message():
        try:
            message = yield proxy.xmit(message)
        except Exception:
            print >>sys.stderr, 'message failed!'

        defer.returnValue(message)
    # end def
    
    def got_message(message):
        print message
    # end def
    ds = []

    d = send_maestro_message()
    d.addCallbacks(got_message)
    ds.append(d)

    dlist = defer.DeferredList(ds, consumeErrors=True)
    dlist.addCallback(lambda res : reactor.stop())

    reactor.run()
# end def

# get scan status, just call a deferLater to poll at a regular inteverval

if __name__ == '__main__':
    maestro_main()
