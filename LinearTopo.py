#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class LinearTopo(Topo):

    def __init__(self, k=2, **opts):
    	super(LinearTopo, self).__init__(**opts)

    self.k = k

    lastSwitch = None
    for i in irange(1, k):
        host = self.addHost('h%s' % i, cpu=.5/k)
        switch = self.addSwitch('s%s' % i)
        linkopts = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
        self.addLink(host, switch, **linkopts)
        if lastSwitch:
            self.addLink(switch, lastSwitch, **linkopts)
        lastSwitch = switch

def perfTest():
    topo = LinearTopo(k=4)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    print "Testing bandwidth between h1 and h4"
    h1, h4 = net.get('h1', 'h4')
    net.iperf((h1, h4))
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    perfTest()
