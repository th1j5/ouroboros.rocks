---
title: "The protocols"
author: "Dimitri Staessens"
#description: protocols
date:  2019-09-06
#type:  page
weight: 20
draft: false
description: >
    A brief introduction to the main protocols.
---

# Network protocol

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

* **Destination address**: This specifies the address to forward the
  packet to. The width of this field is configurable based on various
  preferences and the size of the envisioned network. The Ouroboros
  default is 64 bits. Note that there is _no source address_, this is
  agreed upon during _flow allocation_.

* **Time-to-Live**: Similar to IPv4 and IPv6 (where this field is called
  Hop Limit), this is decremented at each hop to ensures that packets
  don't get forwarded forever in the network, for instance due to
  (transient) loops in the forwarding path. The Ouroboros default for
  the width is one octet (byte).

* **QoS**: Ouroboros supports Quality of Service via a number of methods
  (out of scope for this page), and this field is used to prioritize
  scheduling of the packets when forwarding. For instance, if the
  network gets congested and queues start filling up, higher priority
  packets (e.g. a voice call) get scheduled more often than lower
  priority packets (e.g. a file download). By default this field takes
  one octet.

* **ECN**: This field specifies Explicit Congestion Notification (ECN),
  with similar intent as the ECN bits in the Type-of-Service field in
  IPv4 / Traffic Class field in IPv6. The Ouroboros ECN field is by
  default one octet wide, and its value is set to an increasing value
  as packets are queued deeper and deeper in a congested routers'
  forwarding queues. Ouroboros enforces Forward ECN (FECN).

* **EID**: The Endpoint Identifier (EID) field specified the endpoint for
  which to deliver the packet. The width of this field is configurable
  (the figure shows 16 bits). The values of this field is chosen by
  the endpoints, usually at _flow allocation_. It can be thought of as
  similar to an ephemeral port. However, in Ouroboros there is no
  hardcoded or standardized mapping of an EID to an application.

# Transport protocol

Packet switched networks use transport protocols on top of their
network protocol in order to deal with lost or corrupted packets.

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

* **Flags**: There are 7 flags defined for FRCP.

  - **DATA**: Indicates that the packet is carrying data (this allows
          for 0 length data).

  - **DRF** : Data Run Flag, indicates that there are no unacknowledged
          packets in flight for this connection.

  - **ACK** : Indicates that this packet carries an acknowledgment.
  - **FC**  : Indicates that this packet updates the flow control window.
  - **RDVZ**: Rendez-vous, this is used to break a zero-window deadlock
          that can arise when an update to the flow control window
          gets lost. RDVZ packets must be ACK'd.
  - **FFGM**: First Fragment, this packet contains the first fragment of
          a fragmented payload.
  - **MFGM**: More Fragments, this packet is not the last fragment of a
          fragmented payload.

* **Window**: This updates the flow control window.

* **Sequence Number**: This is a monotonically increasing sequence number
                   used to (re)order the packets at the receiver.

* **Acknowledgment Number**: This is set by the receiver to indicate the
                         highest sequence number that was received in
                         order.

# Operation

The operation of the transport protocol is based on the [Delta-t
protocol](https://www.osti.gov/biblio/5542785-delta-protocol-specification-working-draft),
which is a timer-based protocol that is a bit simpler in operation
than the equivalent functionalities in TCP. In contrast with TCP/IP,
Ouroboros does congestion control purely in the network protocol, and
fragmentation and flow control purely in the transport protocol.