---
title: "Overview"
linkTitle: "Overview"
date: 2019-10-21
weight: 10
description: >
   A bird's eye view of Ouroboros.
---

Ouroboros is a prototype **distributed system** for packetized network
communications. It is a redesign _ab initio_ of the current packet
networking model -- from the programming API ("Layer 7") almost to the
_wire_ ("Layer 1") -- without compromises. This means it's not
directly compatible with anything currently available. It can't simply
be "plugged into" the current network stack. Instead it has some
interfaces into inter-operate with common technologies: run Ouroboros
over Ethernet or UDP, or create tunnels over Ouroboros using tap or
tun devices.

From an application perspective, Ouroboros network operates as a "black
box" with a
[very simple interface](https://ouroboros.rocks/man/man3/flow_alloc.3.html).
Either it provides a _flow_, a bidirectional channel that delivers data
within some requested operational parameters such as delay and
bandwidth and reliability and security; or it provides a broadcast
channel.

From an administrative perspective, an Ouroboros network is a bunch of
_daemons_ that can be thought of as **software routers** (unicast) or
**software _hubs_** (broadcast) that can be connected to each other;
again through
[a simple API](https://ouroboros.rocks/man/man8/ouroboros.8.html).
Each daemon has an address, and they forward packets among each other.
The daemons also implement their own internal name-to-address resolution.

Some of the main _features_ are:

* Ouroboros is minimal: it only sends what it needs to send to operate.

* Ouroboros adheres to the _end-to-end_ principle. Packet headers are
  immutable between the program components (state machines) that
  operate on their state. Only two protocol fields change on a
  hop-by-hop (as viewed within a network layer) basis:
  [TTL and ECN](/docs/concepts/protocols/).

* Ouroboros can establish an encrypted flow in a _single RTT_ (not
  including name-to-address resolution). The flow allocation API is a
  2-way handshake (request-response) that agrees on endpoint IDs and
  performs an ECDHE key exchange. The end-to-end protocol
  [doesn't need a handshake](/docs/concepts/protocols/#operation-of-frcp).

* The Ouroboros end-to-end protocol performs flow control, error
  control and reliable transfer and is implemented as part of the
  _application library_. Sequence numbers, acknowledgments, flow control
  windows... The last thing the application does (or should do) is
  encrypt everything before it hands it to the network layer for
  delivery. With this functionality in the library, it's easy to force
  encryption on _every_ flow that is created from your machine over
  Ouroboros regardless of what the application programmer has
  requested.

* The flow allocation API works as an interface to the network. An
  Ouroboros network layer is therefore "aware" of all traffic that it
  is offered. This allows the layer to shape and police traffic, but
  only based on quantity and QoS, not on the contents of the packets,
  to ensure _net neutrality_.

For a lot more depth, our article on the design of Ouroboros is
accessible on [arXiv](https://arxiv.org/pdf/2001.09707.pdf).

The best place to start understanding a bit what Ouroboros aims to do
and how it differs from other packet networks is to first watch this
presentation at [FOSDEM
2018](https://archive.fosdem.org/2018/schedule/event/ipc/) (it's over
two years old, so not entirely up-to-date anymore), and have a quick
read of the [flow allocation](/docs/concepts/fa/) and [data
path](/docs/concepts/datapath/) sections.

{{< youtube 6fH23l45984 >}}
