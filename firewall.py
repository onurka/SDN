'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

__author__ = "Onur Karaagaoglu, onurka@onurka.com"

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''
import csv


log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''
RULES = []

with open(policyFile) as f:
    next(f)
    rules = csv.reader(f, delimiter=',')
    for rule in rules:
        RULES.append(rule[1:])

class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event, symmetrical = False):    
        ''' Add your logic here ... '''
        sym = 1
        if symmetrical:
            sym = 2

        for rule in RULES:
            for i in range(sym):
                match = of.ofp_match()
                match.dl_src = EthAddr(rule[i%2])
                match.dl_dst = EthAddr(rule[(i+1)%2])
                msg = of.ofp_flow_mod()
                msg.match = match
                event.connection.send(msg)
                log.info("blocking src:%s dst:%s" % (rule[i%2], rule[(i+1)%2]))
    
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)

