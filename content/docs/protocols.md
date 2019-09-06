---
title: "Packet network protocols"
author: "Dimitri Staessens"
description: "protocols"
date:  2019-09-06
#type:  page
draft: false
---

# Network protocols

Packet switched networks move data between two applications using
_network protocols_, which specify where to move the data and how to
do it.  The Internet famously uses the Internet Protocol, IP (versions
4 and 6, which are mutually incompatible, so in essence, there is not
a single Internet, there are two!) as the network protocol that
specifies how to move packets from point _A_ to point _B_.

In order to move a packet from _A_ to _B_, each intermediate node _C_
in the network will investigate the packet header and, based on the
destination address, forward the packet onward until it reaches _B_.

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
[IPv6](https://en.wikipedia.org/wiki/IPv6)).

The most interesting fact about the jump from IPv4 to IPv6 is that the
protocol got noticeably _simpler_.

As Ouroboros tries to preserve privacy as much as possible, it has an
*absolutely minimal network protocol*:

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

The 5 fields in the Ouroboros network protocol are:

* Destination address: This specifies the address to forward the
  packet to. The width of this field is configurable based on various
  preferences and the size of the envisioned network. The Ouroboros
  default is 64 bits. Note that there is _no source address_, this is
  agreed upon during _flow allocation_.

* Time-to-Live: Similar to IPv4 and IPv6 (where this field is called
  Hop Limit), this ensures that packets don't get forwarded forever in
  the network, for instance due to (transient) loops in the forwarding
  path. The Ouroboros default for the width is one octet (byte).

* QoS: Ouroboros supports Quality of Service via a number of methods
  (out of scope for this page), and this field is used to prioritize
  scheduling of the packets when forwarding. For instance, if the
  network gets congested and queues start filling up, higher priority
  packets (e.g. a voice call) get scheduled more often than lower
  priority packets (e.g. a file download). By default this field takes
  one octet.

* ECN: This field specifies Explicit Congestion Notification (ECN),
  with similar intent as the ECN bits in the Type-of-Service field in
  IPv4 / Traffic Class field in IPv6. The Ouroboros ECN field is by
  default one octet wide, and its value is set to an increasing value
  as packets are queued deeper and deeper in a congested routers'
  forwarding queues. Ouroboros enforces Forward ECN (FECN).

* EID: The Endpoint Identifier (EID) field specified the endpoint for
  which to deliver the packet. The width of this field is configurable
  (the figure shows 16 bits). The values of this field is chosen by
  the endpoints, usually at _flow allocation_. It can be thought of as
  similar to an ephemeral port. However, in Ouroboros there is no
  hardcoded or standardized mapping of an EID to an application.

# Transport protocols

Packet switched networks use transport protocols on top of their
[network protocols](/docs/network_protocols) in order to deal with
lost or corrupted packets. IP has the Transport Control Protocol (TCP)
that takes care of things when IP packets get lost. TCP also does some
other neat things, like making sure that a client does not send faster
than a server can process (_flow control_); and making sure that the
network doesn't get overwhelmed by its users (_congestion control_).

The TCP protocol is specified in
[RFC793](https://tools.ietf.org/html/rfc793), and its _header_ is
shown here:

```
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |          Source Port          |       Destination Port        |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                        Sequence Number                        |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                    Acknowledgment Number                      |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |  Data |           |U|A|P|R|S|F|                               |
 | Offset| Reserved  |R|C|S|S|Y|I|            Window             |
 |       |           |G|K|H|T|N|N|                               |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |           Checksum            |         Urgent Pointer        |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                    Options                    |    Padding    |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

The Ouroboros Transport protocol (called the _Flow and Retransmission
Control Protocol_, FRCP) has only 4 fields:

```
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |            Flags              |            Window             |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                        Sequence Number                        |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                    Acknowledgment Number                      |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

```

* Flags: There are 7 flags defined for FRCP.

  - DATA: Indicates that the packet is carrying data (allows for 0
          length data).

  - DRF : Data Run Flag, indicates that there are no unacknowledged
          packets in flight for this connection.

  - ACK : Indicates that this packet carries an acknowledgment.
  - FC  : Indicates that this packet updates the flow control window.
  - RDVZ: Rendez-vous, this is used to break a zero-window deadlock
          that can arise when an update to the flow control window
          gets lost. RDVZ packets must be ACK'd.
  - FFGM: First Fragment, this packet contains the first fragment of
          a fragmented payload.
  - MFGM: More Fragments, this packet is not the last fragment of a
          fragmented payload.

* Window: This updates the flow control window.

* Sequence Number: This is a monotonically increasing sequence number
                   used to (re)order the packets at the receiver.

* Acknowledgment Number: This is set by the receiver to indicate the
                         highest sequence number that was received in
                         order.

---
Changelog:

2019 09 05: Initial version.<br>
2019 09 06: Added section on transport protocol.