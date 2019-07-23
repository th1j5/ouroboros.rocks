---
title: "Creating layers"
author: "Dimitri Staessens"
description: "IRMd"
date:  2019-07-23
#type:  page
draft: false
---

The most important structure in recursive networks are layers, that
are built op from [elements](/docs/elements/) called Inter-Process
Communication Processes (IPCPs).

<center>
{{<figure class="fl w-90"
          src="/images/creating_layers.jpg">}}
</center>

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

<center>
{{<figure class="c w-60"
          src="/images/irm_ipcp_create.png">}}
</center>

The example above creates a unicast IPCP and gives that IPCP a name
(we called it "my_ipcp"). A listing of the IPCPs in the system shows
that the IPCP is running as process 4157, and it is not part of a
layer ("*Not enrolled*").

To create a new functioning network layer, we need to configure the
IPCP, using a primitive called __bootstrapping__. Bootstrapping sets a
number of parameters for the layer (such as the routing algorithm to
use) and activates the IPCP to allow it to start providing flows.  The
Ouroboros command line allows creating an IPCP with some default
values, that are a bit like a vanilla IPv4 network: 32-bit addresses
and shortest-path link-state routing.

<center>
{{<figure class="c w-60"
          src="/images/irm_ipcp_bootstrap.png">}}
</center>

Now, we have a single node-network. In order to create a larger
network, we connect and configure new IPCPs using a third primitive
called __enrollment__. When enrolling an IPCP in a network, it will
create a flow (using a lower layer) to an existing member of the
layer, download the bootstrapping information, and use it to configure
itself as part of this layer.

[TODO: enrollment example]

---
Changelog:

2019-07-23: Initial version
