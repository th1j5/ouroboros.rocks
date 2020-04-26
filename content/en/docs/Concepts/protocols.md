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
*absolutely minimal network protocol*. The field widths are not that
important:

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
 |                              EID                              +
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

The 5 fields in the Ouroboros network protocol are:

* **Destination address**: This specifies the address to forward the
  packet to. The width of this field is configurable based on various
  preferences and the size of the envisioned network. The Ouroboros
  default is 64 bits. Note that there is _no source address_, this is
  agreed upon during _flow allocation_.

* **Time-to-Live**: Similar to IPv4 (in IPv6 this field is replaced by
  the Hop Limit), this is decremented at each hop to ensures that
  packets don't get forwarded forever in the network, for instance due
  to (transient) loops in the forwarding path. The Ouroboros default
  for the width is one octet (byte), limiting the Maximum Packet
  Lifetime in the network to 255 seconds. The initial TTL value for a
  flow can be based on the maximum delay requested by the application.

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

* **EID**: The Endpoint Identifier (EID) field specified the endpoint
  for which to deliver the packet. The width of this field is
  configurable (the figure shows 16 bits). The values of this field is
  chosen by the endpoints, usually at _flow allocation_. It can be
  thought of as similar to an ephemeral port. However, in Ouroboros
  there is no hardcoded or standardized mapping of an EID to an
  application. For security, this field should be sufficiently large.
  For efficiency, it should be easy to map to a flow descriptor at
  the endpoints.

# Flow and retransmission control protocol (FRCP)

Packet switched networks use end-to-end protocols to deal with lost or
corrupted packets. The Ouroboros End-to-End protocol (called the _Flow
and Retransmission Control Protocol_, FRCP) has 4 fields:

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

  - **DRF** : Data Run Flag, indicates that there are no unacknowledged
              packets in flight for this connection.

  - **DATA**: Indicates that the packet is carrying data (this allows
          for 0 length data).

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

* **Sequence Number**, a monotonically increasing sequence number
                       used to (re)order the packets at the receiver.

* **Acknowledgment Number**, set by the receiver to indicate the
                             highest sequence number that has been
                             received in order.

# Operation of FRCP

The operation of FRCP is based on the
[Delta-t protocol](https://www.osti.gov/biblio/5542785-delta-protocol-specification-working-draft),
which is a timer-based protocol that is simpler in operation than the
equivalent ARQ and flow control functionalities in TCP. Watson's
[paper](https://doi.org/10.1016/0376-5075(81)90031-3)
is highly recommended reading; it is truly a thing of beauty.

Before we proceed, a small note on what is meant by _reliability_ in
this discussion. We're going to use the following definition: _if a
piece of a communication is received, all previous pieces of this
communication will be received_. This means data can only be
delivered reliably if it is delivered in-order.

FRCP is only enabled when needed (based on the requested application
QoS). So for a UDP-like operation where packets don't need to be
delivered in order (or at all), Ouroboros doesn't add an FRCP header.
If FRCP is enabled, Ouroboros will track sequence numbers and deliver
packets in-order.

Unreliable delivery: The sender considers all packets as ACK'd. Since
there are no unacknowledged packets, the Data Run Flag is set for all
packets. The receiver tracks the highest received sequence number and
drops all packets that have a lower sequence number. The receiver
never really sends ACKs.

Reliable delivery: The Ouroboros receiver will keep track of a window
of acceptable sequence numbers, indicated by the Left and Right Window
Edges (LWE and RWE). The LWE is thus one greater than the highest
received sequence number, and the receiver always acknowledges with
LWE sequence number. An ACK for a sequence number thus means "I have
received all previous sequence numbers". Received packets with
sequence numbers outside of the window are dropped. If a received
packet has sequence number LWE, both window edges will be incremented
until the LWE reaches a sequence number that has not been received
yet. All the packets that are in the reordering buffer with a sequence
number lower than the new LWE are delivered to the application. If a
received packet has a greater sequence number than LWE but is within
the window, it is stored for reordering.

The reliable delivery has to deal with lost packets,
duplicates,etc. Automated-repeat request handles this: if a packet is
not acknowledged within a certain time-frame, it is retransmitted by
the sender.

For reliable transmission in the presence of lost packets to work,
three timers need to be bounded [^1]. These timers define a "data
run". The state is uni-directional, so for bi-directional
communication, each side has a sender record and a receiver record.

* **MPL**: The maximum packet lifetime. This is bound by the network
           below, using the TTL mechanism. It is approximate with the
           probability of a packet still arriving after MPL close to
           zero.

* **R**: The time after which a packet with a given sequence number
         may not be retransmitted anymore.

* **A**: The maximum time a receiver will wait before acknowledging a
         given sequence number for the first time.

It's not so important when to exactly retransmit a packet, as long as
there are no retransmissions beyond the R timer. Ouroboros -- like TCP
-- estimates average round-trip time (sRTT) and its deviation based on
ACKs. The retranmission timeout (RTO) is set as the sRTT + 2 dev, and
packets are retransmitted after RTO expires, with exponential
back-off. The sRTT is measured with microsecond accuracy[^2] and is
the actual response time of the server application.

If the receiver doesn't hear from the sender for 2MPL + R + A, it may
discard its state. If at this point there are packets received beyond
the LWE at the receiver, the communication has failed in an
unrecoverable way and an error should be returned. From this point,
only packets with DRF will be accepted and they will create a new
receiver state.

If the sender hasn't received an ACK within 2MPL + R + A, the data run
has failed and the sender must stop sending. If the sender has not
received an ACK in 3MPL + R + A, the state associated with this data
can be discarded (failed or not). From this point, new data to send on
the flow will initiate new sender state. This data must be sent with
DRF set and can use a randomly chosen sequence number.

Currently, Ouroboros has one FRCP connection for a flow. In theory
there could be multiple connections supporting a flow, but we haven't
really found a reason for it. In the implementation, the connection
state is initialized with invalidated timers instead of thrown away
and recreated. If a flow is deallocated by the application, care must
be taken that all sent packets are acknowledged or all retransmissions
timed out (so, wait for R timer to expire). Flow deallocation will
also trigger an ACK for the RWE from the receiver (ACKing all packets
that can possibly be in flight, it doesn't care anymore if it receives
more packets).

Flow control works for both reliable and unreliable modes of FRCT. If
flow control is enabled, the receiver will notify the sender of its
Right Window Edge, and the sender keeps track of it. If flow control
is disabled, the sender will just keep sending and received packets
with sequence numbers outside of the receiver window get dropped.

The unreliable mode with flow control can stall on a when an update to
the flow control window gets lost and the sender has reached the
RWE. If the sender has new data to send, it will send a packet with a
Rendez-Vous (RDVZ) bit set. RDVZ packets must always be acknowledged
(so they can be retransmitted). This requires a backoff
mechanism. Note that the rendez-vous mechanism is just a way of being
'nice'; it's not really needed, since the request was for an
unreliable flow and there is no delivery guarantee.

The last mechanism in FRCP is fragmentation. Messages that are too
large to be transmitted on the supporting flow are split up in
different packets, called "fragments"[^3]. These are marked with two
bits. First fragment (FFGM), and More fragments (MFGM). A message that
fits in a single packet has the FFGM | MFGM bits set to "10". If a
message is fragmented, it will have a sequence of packets with the
bits set to "11" for the first fragment, "01" for intermediate
fragments and "00" for the last fragment. Single-bit fragmentation
(e.g. only a MFGM bit) is more minimalistic , but it discards two
consecutive messages if the last fragment of the first message is
lost. This is just being 'nice' at little cost.

We can't stress this enough: Ouroboros has this mechanism implemented
in the application. The (simple) logic is executed as part of the
read/write operations. **FRCP is in "the application", not in "the
network"**[^4]. If a packet is acknowledged, it is received by the remote
program, not possibly waiting in some buffer still to be delivered. If
an application crashes, it means all associated state at that endpoint
is gone and a new higher-level flow will need to be established. If a
program requests encryption, the entire FRCP header is encrypted. This
is probably the best course of action to protect against replay
attacks or other attacks based on guessing sequence numbers. Note that
the size of the sequence number space should be at least (2MPL + R +
A) * T, where T is the number of sequence numbers generated in a
certain unit of time.

[^1]: This was proven by Watson in [Timer-Based Mechanisms in Reliable Transport Protocol Connection Management](https://doi.org/10.1016/0376-5075(81)90031-3). TCP also has these three timers bounded.
[^2]: Fast retransmit methods (retransmitting if a number of consecutive ACKs with the same sequence number are received) can still be useful. Underestimation of sRTT has little impact on throughput apart from possible unnecessary traffic duplication (the additional packets also update the RTT estimate). In Ouroboros, congestion avoidance is the responsability of the flow allocator.
[^3]: IPv4 and IPv6 fragmentation makes for some rather amusing reading.
[^4]: This doesn't mean it can't be implemented in hardware.
