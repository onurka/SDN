'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

__author__ = "Onur Karaagaoglu, onurka@onurka.com"

from mininet.topo import Topo

class CustomTopo(Topo):
    '''
    Simple Data Center Topology.

    linkopts - (1:core, 2:aggregation, 3: edge) parameters
    fanout - number of child switch per parent switch.
    '''
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        # Add your logic here ...
        self.linkopts1 = linkopts1
        self.linkopts2 = linkopts2
        self.linkopts3 = linkopts3
        self.fanout = fanout
        self.switch_index = 1
        self.host_index = 1

        self.create_tree([linkopts1, linkopts2, linkopts3], fanout)

    def create_tree(self, linkopts, fanout, depth = 0, tier = 3):
        '''
        Function to create tree nodes.
        '''
        is_switch = depth < tier
        if is_switch:
            node = self.addSwitch("s%s" % self.switch_index)
            self.switch_index += 1
            for i in xrange(fanout):
                child_node = self.create_tree(linkopts, fanout, depth + 1)
                self.addLink(node, child_node, **linkopts[depth])
        else:
            node = self.addHost("h%s" % self.host_index)
            self.host_index += 1

        return node 
                            
topos = { 'custom': ( lambda: CustomTopo() ) }

