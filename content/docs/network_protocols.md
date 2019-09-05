---
title: "Packet network protocols"
author: "Dimitri Staessens"
description: "what"
date:  2019-09-05
#type:  page
draft: false
---

Packet switched networks move data between two applications using
_protocols_, which specify where to move the data and how to do it.
The Internet famously uses the Internet Protocol, IP (versions 4 and
6, which are mutually incompatible, so in essence, there is not a
single Internet, there are two!) as the network protocol that
specifies how to move packets from point _A_ to point _B_. On top, it
has the Transport Control Protocol (TCP) that takes care of things
when IP packets get lost. TCP also does some other neat things, like
making sure that a client does not send faster than a server can
process, usually called _flow control_; and making sure that the
network doesn't get overwhelmed by its users, usually called
_congestion control_.

The IPv4 protocol is specified in
[RFC791](https://tools.ietf.org/html/rfc791), and its _header_ is
shown here:

```
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |Version|  IHL  |Type of Service|          Total Length         |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |         Identification        |Flags|      Fragment Offset    |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |  Time to Live |    Protocol   |         Header Checksum       |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                       Source Address                          |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                    Destination Address                        |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                    Options                    |    Padding    |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

The IPv6 protocol is specified in
[RFC2460](https://tools.ietf.org/html/rfc2460), and its header format
is:

```
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |Version| Traffic Class |           Flow Label                  |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |         Payload Length        |  Next Header  |   Hop Limit   |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                                                               |
 +                                                               +
 |                                                               |
 +                         Source Address                        +
 |                                                               |
 +                                                               +
 |                                                               |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                                                               |
 +                                                               +
 |                                                               |
 +                      Destination Address                      +
 |                                                               |
 +                                                               +
 |                                                               |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

```

For a detailed description of what all the fields in this protocol
mean, we gladly refer you to the RFCs or the wikipedia pages (
[IPv4](https://en.wikipedia.org/wiki/IPv4) and
[IPv6](https://en.wikipedia.org/wiki/IPv6)).  The most interesting
fact about the jump from IPv4 to IPv6 is that the protocol got
noticeably simpler.

As Ouroboros tries to preserve privacy as much as possible, it has an
*absolutely minimal network protocol* (it's also configurable, this is
the 64 bit address, 16 bit EID version):

```
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                                                               |
 +                      Destination Address                      +
 |                                                               |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 | Time-to-Live  |      QoS      |     ECN       |     EID       |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |      EID      |
 +-+-+-+-+-+-+-+-+
```

The fields are:

* Destination address: This specifies the address to forward the
  packet to. The width of this field is configurable based on various
  preferences and the size of the envisioned network. The Ouroboros
  default is 64 bits. Note that there is _no source address_, this is
  agreed upon during _flow allocation_.

* Time-to-Live: Similar to IPv4 and IPv6 (where this field is called
  Hop Limit), this ensures that packets don't get forwarded forever in
  the network, for instance due to (transient) loops in the forwarding
  path.

* QoS: Ouroboros supports Quality of Service via a number of methods
  (out of scope for this page), and this field is used to prioritize
  scheduling of the packets when forwarding. For instance, if the
  network gets congested and queues start filling up, higher priority
  packets (e.g. a voice call) get scheduled more often than lower
  priority packets (e.g. a file download).

* ECN: This field specifies Explicit Congestion Notification (ECN),
  with similar intent as the ECN bits in the DSCP field in IPv4 / ToS
  field in IPv6. It has 8-bit width as a default, and gets set higher
  as packets are deeper and deeper in a forwarding queue. Ouroboros
  enforces Forward ECN (FECN).

* EID: The Endpoint Identifier (EID) field specified the endpoint for
  which to deliver the packet. The width of this field is
  configurable, the values of this field is chosen by the endpoints at
  _flow allocation_. It can be thought of as an ephemeral port.

---
Changelog:

2019 09 05: Initial version.