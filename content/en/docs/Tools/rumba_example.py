from rumba.model import Node, NormalDIF, ShimEthDIF

# import testbed plugins
import rumba.testbeds.jfed as jfed
import rumba.testbeds.local as local

# import Ouroboros prototype plugin
import rumba.prototypes.ouroboros as our

__all__ = ["local_exp", "nodes"]

n1 = NormalDIF("n1")
e1 = ShimEthDIF("e1")
e2 = ShimEthDIF("e2")
e3 = ShimEthDIF("e3")

clientNode1 = Node("client1",
                   difs=[e1, n1],
                   dif_registrations={n1: [e1]})

clientNode2 = Node("client2",
                   difs=[e3, n1],
                   dif_registrations={n1: [e3]})

routerNode = Node("router",
                  difs=[e1, e2, e3, n1],
                  dif_registrations={n1: [e1, e2, e3]})

serverNode = Node("server",
                  difs=[e2, n1],
                  dif_registrations={n1: [e2]})

nodes = ["client1", "client2", "router", "server"]

local_tb = local.Testbed()

local_exp = our.Experiment(local_tb,
                           nodes=[clientNode1,
                                  clientNode2,
                                  routerNode,
                                  serverNode])
