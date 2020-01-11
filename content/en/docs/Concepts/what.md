---
title: "Recursive networks"
author: "Dimitri Staessens"

date:  2020-01-11
weight: 2
description: >
   The recursive network paradigm
---

The functional repetition in the network stack is discussed in
detail in the book __*"Patterns in Network Architecture: A Return to
Fundamentals"*__. From the observations in the book, a new architecture
was proposed, called the "__R__ecursive __I__nter__N__etwork
__A__rchitecture", or [__RINA__](http://www.pouzinsociety.org).

__Ouroboros__ follows the recursive principles of RINA, but deviates
quit a bit from its internal design. There are resources on the
Internet explaining RINA, but here we will focus
on its high level design and what is relevant for Ouroboros.

Let's look at a simple scenario of an employee contacting an internet
corporate server over a Layer 3 VPN from home. Let's assume for
simplicity that the corporate LAN is not behind a NAT firewall. All
three networks perform (among some other things):

__Addressing__: The VPN hosts receive an IP address in the VPN, let's
say some 10.11.12.0/24 address. The host will also have a public IP
address, for instance in the 20.128.0.0/16 range . Finally that host
will have an Ethernet MAC address. Now the addresses __differ in
syntax and semantics__, but for the purpose of moving data packets,
they have the same function: __identifying a node in a network__.

__Forwarding__: Forwarding is the process of moving packets to a
destination __with intent__: each forwarding action moves the data
packet __closer__ to its destination node with respect to some
__metric__ (distance function).

__Network discovery__: Ethernet switches learn where the endpoints are
through MAC learning, remembering the incoming interface when it sees
a new soure address; IP routers learn the network by exchanging
informational packets about adjacency in a process called *routing*;
and a VPN proxy server relays packets as the central hub of a network
connected as a star between the VPN clients and the local area
network (LAN) that is provides access to.

__Congestion management__: When there is a prolonged period where a
node receives more traffic than can forward forward, for instance
because there are incoming links with higher speeds than some outgoing
link, or there is a lot of traffic between different endpoints towards
the same destination, the endpoints experience congestion. Each
network could handle this situation (but not all do: TCP does
congestion control for IP networks, but Ethernet just drops traffic
and lets the IP network deal with it. Congestion management for
Ethernet never really took off).

__Name resolution__: In order not having to remember addresses of the
hosts (which are in a format that make it easier for a machine to deal
with), each network keeps a mapping of a name to an address. For IP
networks (which includes the VPN in our example), this is done by the
Domain Name System (DNS) service (or, alternatively, other services
such as *open root* or *namecoin*). For Ethernet, the Address
Resolution Protocol maps a higher layer name to a MAC (hardware)
address.

{{<figure width="50%" src="/docs/concepts/layers.jpg">}}

Recursive networks take all these functions to be part of a network
layer, and layers are mostly defined by their __scope__. The lowest
layers span a link or the reach of some wireless technology. Higher
layers span a LAN or the network of a corporation e.g. a subnetwork or
an Autonomous System (AS). An even higher layer would be a global
network, followed by a Virtual Private Network and on top a tunnel
that supports the application. Each layer being the same in terms of
functionality, but different in its choice of algorithm or
implementation. Sometimes the function is just not implemented
(there's no need for routing in a tunnel!), but logically it could be
there.
