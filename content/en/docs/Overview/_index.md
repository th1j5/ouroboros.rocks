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
networking model -- from the programming API almost to the wire --
without compromises. While the prototype not directly compatible with
IP or sockets, it has some interfaces to be interoperable with common
technologies: we run Ouroboros over Ethernet or UDP, or create
IP/Ethernet tunnels over Ouroboros by exposing tap or tun devices.

From an application perspective, an Ouroboros network is a "black box"
with a
[simple interface](https://ouroboros.rocks/man/man3/flow_alloc.3.html).
Either Ouroboros will provides a _flow_, a bidirectional channel that delivers
data within some requested operational parameters such as delay and
bandwidth and reliability and security; or it provides a broadcast
channel to a set of joined programmes.

From an administrative perspective, an Ouroboros network is a bunch of
_daemons_ that can be thought of as **software routers** (unicast) or
**software _hubs_** (broadcast) that can be connected to each other;
again through
[a simple API](https://ouroboros.rocks/man/man8/ouroboros.8.html).

Some of the main characteristics are:

* Ouroboros is <b>minimalistic</b>: it has only the essential protocol
  fields. It will also try to use the lowest possible network layer
  (i.e. on a single machine, Ouroboros communicates directly over
  shared memory, over a LAN it will communicate over Ethernet, over IP
  it will communicate over UDP), in a completely transparent way to
  the application.

* Ouroboros enforces the _end-to-end_ principle. Packet headers are
  <b>immutable</b> between the state machines that operate on their
  state. Only two protocol fields change on a hop-by-hop (as viewed
  within a network layer) basis: [TTL and
  ECN](/docs/concepts/protocols/). This immutability can be enforced
  through authentication (not yet implemented).

* Ouroboros has _external_ and _dynamic_ server application
  binding. Socket applications leave it to the application developer
  to manage binding from within the program (typically a bind() call
  to either a specific IP address or to all addresses (0.0.0.0),
  leaving all configuration application (or library-) specific. When
  shopping for network libraries, a typical questions are "can it bind
  to multiple IP addresses?".

  Ouroboros makes all this management external to the program: server
  applications only need to call flow_accept(). The _bind()_ primitive
  allows a program (or running process) to be bound from the command
  line to a certain (set of) service names and when a flow request
  arrives for that service, Ouroboros acts as a broker that hands of
  the flow to any program that is bound to that service. Binding is
  N-to-M: multiple programs can be bound to the same service name, and
  programs can be bound to multiple names. This binding is also
  _dynamic_: it can be done while the program is running, and will not
  disrupt existing flows.

  In addition, the _register()_ primitive allows external and dynamic
  control over which network a service name is available over. Again,
  while the service is running, and without disrupting existing flows.

* The Ouroboros end-to-end protocol performs flow control, error
  control and reliable transfer and is implemented as part of the
  _application library_. This includes sequence numbering, ordering,
  sending and handling acknowledgments, managing flow control windows,
  ...

* Ouroboros can establish an encrypted flow in a _single RTT_ (not
  including name-to-address resolution). The flow allocation API is a
  2-way handshake (request-response) that agrees on endpoint IDs and
  performs an ECDHE key exchange. The end-to-end protocol is based on
  Delta-t and
  [doesn't need a handshake](/docs/concepts/protocols/#operation-of-frcp).

* Ouroboros allows encrypting everything before handing it to the next
  layer for delivery. With this functionality in the library, it's
  easy to force encryption on _every_ flow that is created from your
  machine over Ouroboros regardless of what the application programmer
  has implemented. Unlike TLS, the end-to-end header (sequence number
  etc) can be fully encrypted.

* Ouroboros congestion control operates at the network level. It does
  not (_can not!_) rely on acknowledgements. This means all network
  flows are automatically congestion controlled.

* The flow allocation API works as an interface to the network. An
  Ouroboros network layer is therefore "aware" of all traffic that it
  is offered. This allows the layer to implement shaping and police
  traffic, but only based on quantity and QoS, not on the contents of
  the packets, to ensure _net neutrality_.

For a lot more depth, our article on the design of Ouroboros is
accessible on [arXiv](https://arxiv.org/pdf/2001.09707.pdf).

The best place to start understanding a bit what Ouroboros aims to do
and how it differs from other packet networks is to first watch this
presentation at [FOSDEM
2018](https://archive.fosdem.org/2018/schedule/event/ipc/) but note
that this presentation is over three years old, and very outdated in
terms of what has been implemented. The prototype implementation is
now capable of asynchronous flows handling, doing retransmission, flow
control, congestion control...

The next things to do are to have a quick read of the
[flow allocation](/docs/concepts/fa/)
and
[data path](/docs/concepts/datapath/)
sections.

{{< youtube 6fH23l45984 >}}
