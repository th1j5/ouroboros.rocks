---
title: "Recursive layers"
author: "Dimitri Staessens"
#description: "IRMd"
date:  2019-07-23
weight: 20
#type:  page
draft: false
description: >
    How to build a recursive network.
---

The most important structure in recursive networks are the layers,
that are built op from [elements](/docs/elements/) called
Inter-Process Communication Processes (IPCPs). (Note again that the
layers in recursive networks are not the same as layers in the OSI
model).

{{<figure width="50%" src="/docs/concepts/creating_layers.jpg">}}

Now, the question is, how do we build these up these layers? IPCPs are
small programs (think of small virtual routers) that need to be
started, configured and managed. This functionality is usually
implemented in some sort of management daemon. Current RINA
implementations call it the *IPC manager*, Ouroboros calls it the
__IPC Resource Management daemon__ or __IRMd__ for short. The IRMd
lies at the heart of each system that is participating in an Ouroboros
network, implementing the core function primitives. It serves as the
entry point for the system/network administrator to manage the network
resources.

We will describe the functions of the Ouroboros IRMd with the
Ouroboros commands for illustration and to make things a bit more
tangible.

The first set of primitives, __create__ (and __destroy__), allow
creating IPCPs of a given *type*. This just runs the process without
any further configuration. At this point, that process is not part of
any layer.

```
$ irm ipcp create type unicast name my_ipcp
$ irm ipcp list
+---------+----------------------+------------+----------------------+
|     pid |                 name |       type |                layer |
+---------+----------------------+------------+----------------------+
|    7224 |              my_ipcp |    unicast |         Not enrolled |
+---------+----------------------+------------+----------------------+
```

The example above creates a unicast IPCP and gives that IPCP a name
(we called it "my_ipcp"). A listing of the IPCPs in the system shows
that the IPCP is running as process 7224, and it is not part of a
layer ("*Not enrolled*").

To create a new functioning network layer, we need to configure the
IPCP, using a primitive called __bootstrapping__. Bootstrapping sets a
number of configuration optionss for the layer (such as the routing
algorithm to use) and activates the IPCP to allow it to start
providing flows.  The Ouroboros command line allows creating an IPCP
with some default values, that are a bit like a vanilla IPv4 network:
32-bit addresses and shortest-path link-state routing.

```
$ irm ipcp bootstrap name my_ipcp layer my_layer
$ irm ipcp list
+---------+----------------------+------------+----------------------+
|     pid |                 name |       type |                layer |
+---------+----------------------+------------+----------------------+
|    7224 |              my_ipcp |    unicast |             my_layer |
+---------+----------------------+------------+----------------------+
```

Now we have a single node-network. In order to create a larger
network, we connect and configure new IPCPs using a third primitive
called __enrollment__. When enrolling an IPCP in a network, it will
create a flow (using a lower layer) to an existing member of the
layer, download the bootstrapping information, and use it to configure
itself as part of this layer.

The final primitive is the __connect__ (and __disconnect__)
primitive. This allows to create *adjacencies* between network nodes.

An example of how to create a small two-node network is given in
[tutorial 2](/docs/tutorials/tutorial-2/)
