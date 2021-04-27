---
title: "The Ouroboros model"
author: "Dimitri Staessens"

date:  2020-04-07
weight: 2
description: >
   Computer Network fundamentals
---

```
Computer science is as much about computers as astronomy is
about telescopes.
  -- Edsger Wybe Dijkstra
```

The model for computer networks underlying the Ouroboros prototype is
the result of a long process of gradual increases in my understanding
of the core principles that underly computer networks, starting from
my work on traffic engineering packet-over-optical networks using
Generalized Multi-Protocol Label Switching (G/MPLS) and Path
Computation Element (PCE), then Software Defined Networks (SDN), the
work with Sander investigating the Recursive InterNetwork Architecture
(RINA) and finally our implementation of what would become the
Ouroboros Prototype. The way it is presented here is not a reflection
of this long process, but a crystalization of my current understanding
of the Ouroboros model.

During most of my PhD work at the engineering department, I spent my
research time on modeling telecommunications networks and computer
networks as _graphs_. The nodes represented some switch or router --
either physical or virtual --, the links represented a cable or wire
-- again either physical or virtual -- and then the behaviour of
various technologies were simulated on those graphs to develop
algorithms that analyze some behaviour or optimize some or other _key
performance indicator_ (KPI). This line of reasoning, starting from
_networked devices_ is how a lot of research on computer networks is
conducted. But what happens if we turn this upside down, and develop a
_universal_ model for computer networks starting from some very basic
elements?

### Two defining elements

The Ouroboros model postulates that there are only 2 possible methods
of distributing packets in a network layer: _FORWARDING_ packets based
on some label identifying a node[^1], or _FLOODING_ packets on all
links but the incoming link.

We call an element that forwards a __forwarding element__,
implementing a _packet forwarding function_ (PFF). The PFF has as
input a destination label (in graph theory, a _vertex_), and as output
a set of output links (in graph theory, _arcs_) on which the incoming
packet with that label is to be forwarded on. The destination label
needs to be in a packet header.

We call an element that floods a __flooding element__, and it
implements a packet flooding fuction. It is completely stateless, and
has a input the incoming arc, and as output all non-incoming
arcs. This is all local information, so packets on a broadcast layer
do not need a header at all.

{{<figure width="40%" src="/docs/concepts/model_elements.png">}}

Peering relationships are only allowed between forwarding elements, or
between flooding elements, but never between a forwarding element and
a flooding element. We call a connected graph consisting of nodes that
hold forwarding elements a __unicast layer__, and similary we call a
connected _tree_[^2] consisting of nodes that house a flooding element
a __broadcast layer__.

The objective for the Ouroboros model is to hold for _all_ packet
networks; our __conjecture__ is that __all functioning packet-switched
network technologies can be decomposed into finite sets of unicast and
broadcast layers__. Unicast and broadcast layers can be easily found
in TCP/IP, Recursive InterNetworking Architecture (RINA), Delay
Tolerant Networks (DTN), Ethernet, VLANs, Loc/Id split (LISP),...
[^3]. The Ouroboros _model_ by itself is not recursive. What is known
as _recursive networking_ is a choice to use a single standard API to
interact with all unicast layers and a single standard API to interact
with all broadcast layers[^4].

### The unicast layer

A unicast is a collection of interconnected forwarding elements. A
unicast layer provides a best-effort unicast packet service between
two endpoints in the layer. We call the abstraction of this
point-to-point unicast service a flow. A flow in itself has no
guarantees in terms of reliability [^5].

{{<figure width="70%" src="/docs/concepts/unicast_layer.png">}}

A representation of a unicast layer is drawn above, with a flow
between the _green_ (bottom left) and _red_ (top right) forwarding
elements.

The forwarding function operates in such a way that, given the label
of the destination node (in the case of the figure, a _red_ label),
the packet will move to the destination node (_red_) in a _deliberate_
manner. The paper has a precise mathematical definition, but
qualitatively, our definition of _FORWARDING_ ensures that the
trajectory that packets follow through a network layer between source
and destination

* doesn't need to use the 'shortest' path
* can use multiple paths
* can use different paths for different packets
* can involve packet duplication
* will not have loops[^6] [^7]

{{<figure src="https://latex.codecogs.com/svg.latex?\Large&space;x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}">}}

### The broadcast layer

A broadcast layer is a collection of interconnected flooding
elements. The nodes can have either, both or neither of the sender and
receiver role. A broadcast layer provides a best-effort broadcast
packet service from sender nodes to all (receiver) nodes in the layer.

{{<figure width="70%" src="/docs/concepts/broadcast_layer.png">}}

Our simple definition of _FLOODING_ -- given a set of adjacent links,
send packets received on a link in the set on all other links in the
set -- has a huge implication the properties of a fundamental
broadcast layer: the graph always is a _tree_, or packets could travel
along infinite trajectories with loops [^8].

### Building layers

We now define the fundamental operations on packet network
layers. These operations can be implemented through manual
configuration or automated protocol interactions. They can be skipped
(no-operation, (nop)) or involve complex operations such as
authentication.

The construction of (unicast and broadcast) layers involves 2
fundamental operations: adding a node to a layer is called
_enrollment_. Enrollment prepares a node to act as a functioning
element of the layer, exchanging the key parameters for a layer. It
can involve authentication, and setting roles and permissions. After
enrollment, we may add peering relationships by creating adjacencies
between forwarding elements in a unicast layer or between flooding
elements in a broadcast layer. We termed this _adjacency
management_. The inverse operations are called _unenrollment_ and
_tearing down_ adjacencies between elements.

Operations such as merging and splitting layers can be decomposed into
these two operations. This doesn't mean that merge operations
shouldn't be researched. To the contrary, optimizing this is
instrumental for creating networks practical on a global scale.

It is immediately clear that these operations are very broadly
defined, and can be implemented in a myriad of ways. The main
objective of these definitions - and the Ouroboros model as a whole --
is to separate __mechanism__ (the _what_) from __policy__ (the _how_)
so that we have a _consistent_ framework for _reasoning_ about
protocols and functionality in computer networks.

### Under construction ...


[^1]: This identifier can be thought of as an address, the identified
      node is a _forwarding element_.

[^2]: A tree is a connected graph with N vertices and N-1 edges.

[^3]: I've already explored how some technologies map to the Ouroboros
      model in my blog post on
      [unicast vs multicast](/blog/2021/04/02/how-does-ouroboros-do-anycast-and-multicast/).

[^4]: Of course, once the model is properly understood and a
      green-field scenario is considered, recursive networking is the
      obvious choice, and so the Ouroboros prototype _is_ a recursive
      network.

[^5]: This is where Ouroboros is similar to IP, and differs from RINA.
      RINA layers (DIFs) aim to provide reliability as part of the
      service (flow). We found this approach in RINA to be severely
      flawed, preventing RINA to be a _universal_ model for all
      networking and IPC. RINA can be modeled as an Ouroboros network,
      but Ouroboros cannot be modeled as a RINA network. I've written
      about this in more detail about this in my blog post on
      [Ouroboros vs RINA](/blog/2021/03/20/how-does-ouroboros-relate-to-rina-the-recursive-internetwork-architecture/).

[^6]: Transient loops are loops that occur due to forwarding functions
      momentarily having different views of the network graph, for
      instance due to delays in disseminating information on
      unavailable links.

[^7]: Some may think that it's possible to build a network layer that
      forwards packets in a way that _deliberately_ takes a couple of
      loops between a set of nodes and then continues forwarding to
      the destination, violating the definition of _FORWARDING_. It's
      not possible, because based on the destination address alone,
      there is no way to know whether that packet came from the loop
      or not. _"But if I add a token/identifier/cookie to the packet
      header"_ -- yes, that is possible, and it may _look like that
      packet is traversing a loop_ in the network, but it doesn't
      violate the definition. The question is: what is that
      token/identifier/cookie naming? It can be only one of a couple
      of things: a node, a link or a layer. Adding a token and the
      associated logic to process it, will be equivalent to adding
      nodes to the layer (modifying the node name space to include
      that token) or adding another layer. In essence, the
      implementation of the nodes on the loop will be doing something
      like this:

      ```
      if logic_based_on_token:
          # behave like node (token, X)
      else if logic_based_on_token:
          # behave like node (token, Y)
      else  # and so on
      ```

      When taking the transformation into account the resulting
      layer(s) will follow the fundamental model as it is presented
      above. Also observe that adding such tokens may drastically
      increase the address space in the fundemental representation.

[^8]: Is it possible to broadcast on a non-tree graph by pruning in
      some way, shape or form? There are some things to
      consider. First, if the pruning is done to eliminate links in
      the graph, let's say in a way that STP prunes links on an
      Ethernet or VLAN, then this is operation is equivalent creating
      a new broadcast layer. We call this enrollment and adjacency
      management. This will be explained in the next sections. Second
      is trying to get around loops by adding the name of the (source)
      node plus a token/identifier/cookie as a packet header in order
      to detect packets that have traveled in a loop, and dropping
      them when they do. This kind of network doesn't fit neither the
      broadcast layer nor the unicast layer. But the thing is: it also
      _doesn't work_ at any reasonable scale, as all packets need to
      be tracked, at least in theory, forever. Assuming packet
      ordering is preserved inside a layer a big no-no. Another line
      of thinking may be to add a decreasing counter to avoid loops,
      but it goes down a similar rabbit hole. How large to set the
      counter? This also doesn't scale. These solution may work for
      some use cases, but they don't work _in general_.
