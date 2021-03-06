def maestro_main(host):
    from twisted.internet.protocol import ClientCreator
    from twisted.conch.telnet import Telnet
    from twisted.internet import reactor
    
    class MyTelnet(Telnet):
        def connectionMade(self):
            print "connected!\n"
        def dataReceived(self, data):
            print data
            if "MAESTRO" in data:
                d = self._write("quit\n")

        def connectionLost(self, reason):
            reactor.stop()
            print "done."

    mytelnet = ClientCreator(reactor, MyTelnet)
    d = mytelnet.connectTCP(host, 23)
    reactor.run()
    
if __name__ == '__main__':
    maestro_main('10.0.0.56')
