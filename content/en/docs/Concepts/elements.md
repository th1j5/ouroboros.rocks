---
title: "Elements of a recursive network"
author: "Dimitri Staessens"
date:  2019-07-11
weight: 2
description: >
    The building blocks for recursive networks.
---

This section describes the high-level concepts and building blocks are
used to construct a decentralized [recursive network](/docs/what):
layers and flows. (Ouroboros has two different kinds of layers, but
we will dig into all the fine details in later posts).

A __layer__ in a recursive network embodies all of the functionalities
that are currently in layers 3 and 4 of the OSI model (along with some
other functions). The difference is subtle and takes a while to get
used to (not unlike the differences in the term *variable* in
imperative versus functional programming languages). A recursive
network layer handles requests for communication to some remote
process and, as a result, it either provides a handle to a
communication channel -- a __flow__ endpoint --, or it raises some
error that no such flow could be provided.

A layer in Ouroboros is built up from a bunch of (identical) programs
that work together, called Inter-Process Communication (IPC) Processes
(__IPCPs__). The name "IPCP" was first coined for a component of the
[LINCS]
(https://www.osti.gov/biblio/5542785-delta-protocol-specification-working-draft)
hierarchical network architecture built at Lawrence Livermore National
Laboratories and was taken over in the RINA architecture. These IPCPs
implement the core functionalities (such as routing, a dictionary) and
can be seen as small virtual routers for the recursive network.

{{<figure width="60%" src="/docs/concepts/rec_netw.jpg">}}

In the illustration, a small 5-node recursive network is shown. It
consists of two hosts that connect via edge routers to a small core.
There are 6 layers in this network, labelled __A__ to __F__.

On the right-hand end-host, a server program __Y__ is running (think a
mail server program), and the (mail) client __X__ establishes a flow
to __Y__ over layer __F__ (only the endpoints are drawn to avoid
cluttering the image).

Now, how does the layer __F__ get the messages from __X__ to __Y__?
There are 4 IPCPs (__F1__ to __F4__) in layer __F__, that work
together to provide the flow between the applications __X__ and
__Y__. And how does __F3__ get the info to __F4__? That is where the
recursion comes in. A layer at some level (its __rank__), will use
flows from another layer at a lower level. The rank of a layer is a
local value. In the hosts, layer __F__ is at rank 1, just above layer
__C__ or layer __E_. In the edge router, layer __F__ is at rank 2,
because there is also layer __D__ in that router. So the flow between
__X__ and __Y__ is supported by flows in layer __C__, __D__ and __E__,
and the flows in layer __D__ are supported by flows in layers __A__
and __B__.

Of course these dependencies can't go on forever. At the lowest level,
layers __A__, __B__, __C__ and __E__ don't depend on a lower layer
anymore, and are sometimes called 0-layers. They only implement the
functions to provide flows, but internally, they are specifically
tailored to a transmission technology or a legacy network
technology. Ouroboros supports such layers over (local) shared memory,
over the User Datagram Protocol, over Ethernet and a prototype that
supports flows over an Ethernet FPGA device. This allows Ouroboros to
integrate with existing networks at OSI layers 4, 2 and 1.

If we then complete the picture above, when __X__ sends a packet to
__Y__, it passes it to __F3__, which uses a flow to __F1__ that is
implemented as a direct flow between __C2__ and __C1__. __F1__ then
forwards the packet to __F2__ over a flow that is supported by layer
__D__. This flow is implemented by two flows, one from __D2__ to
__D1__, which is supported by layer A, and one from __D1__ to __D3__,
which is supported by layer __B__. __F2__ will forward the packet to
__F4__, using a flow provided by layer __E__, and __F4__ then delivers
the packet to __Y__.  So the packet moves along the following chain of
IPCPs: __F3__ --> __C2__ --> __C1__ --> __F1__ --> __D2__ --> __A1__
--> __A2__ --> __D1__ --> __B1__ --> __B2__ --> __D3__ --> __F2__ -->
__E1__ --> __E2__ --> __F4__.

{{<figure width="40%" src="/docs/concepts/dependencies.jpg">}}

A recursive network has __dependencies__ between layers in the
network, and between IPCPs in a __system__. These dependencies can be
represented as a directed acyclic graph (DAG). To avoid problems,
these dependencies should never contain cycles (so a layer I should
not directly or indirectly depend on itself). The rank of a layer is
defined (either locally or globally) as the maximum depth of this
layer in the DAG.
