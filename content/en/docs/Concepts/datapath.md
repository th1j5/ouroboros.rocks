---
title: "The Ouroboros datapath (unicast)"
author: "Dimitri Staessens"
#description: datapath
date:  2020-01-18
weight: 40
draft: false
description: >
     What happens when you do a flow_write()/flow_read()?
---

The Ouroboros datapath is responsibe for all key functions that allow
Ouroboros to transfer data reliably, securely and privately from one
process to another. So, in essence, to perform [Inter-Process
Communication](https://en.wikipedia.org/wiki/Inter-process_communication).
How this datapath is bootstrapped is covered in the [Flow
Allocation](../fa/) section.

This page provides an overview of the journey of a piece of data that
is sent over Ouroboros. It covers one layer in the recursive network.

{{<figure width="80%" src="/docs/concepts/datapath.png">}}

The _flow\_alloc()_ call bootstraps the datapath and configures which
functions will be performed on the packet. This will be symmetrical at
the receiver side and sender side. The way this is is done is based on
a __qos parameter__. We won't go into all its details here, but in
essence it allows enabling or disabling some __end-to-end__ functions.

These functions are

- __fragmentation/reassembly__: when the data is too big for the
 network to transport in one chunck, it will first be chopped into
 smaller pieces, and reassembled at the endpoint. The maximum limit is
 calculated by the IPCP as part of flow allocation. There are two bits
 used for fragmentation, a _first fragment bit_, and a _more
 fragments_ bit.

- __sequencing/reordering__: packets are assigned a sequence number so
 they can be delivered in the same order as they are sent. Sequence
 numbers increase by 1 _per fragment_.

-  __flow control__: this prevents the source process from sending
 faster than the receiving process can handle[^1].

- __automated repeat/request (ARQ)__: When a packet is received, the
 receiver will send and acknowledgment (ACK). If an acknowledmgent is
 not received in a certain timeframe (based on the estimated
 round-trip time and its standard deviation), the sender will
 retransmit it.

The above four functions are grouped together in the FRCP [transport
protocol](../protocols/#transport-protocol). The protocol can be
disabled in its entirety: Ouroboros delivers packets as they arrive,
doesn't recover lost packets, drops packets that are too big,
etc.). When FRCP is disabled, the headers are not even added to the
packet. From the perspective of the endpoints, this is similar in
service to UDP/IP. Or some functions can be disabled separately, such
as ARQ, then you have something like UDP but with flow control. We
will not go into the details of the operation of FRCP here.

- __authentication__: A message authentication code is appended to the message.
- __encryption__: The message is encrypted before sending.

These two functions (authentication/encryption) can be enabled or
disabled separately and enabling both should allow Encrypt-then-MAC,
Encrypt-and-MAC and MAC-and-encrypt[^2].

All the above functions are implemented in the _Ouroboros library_. So
they are executed by the application.

Let's start with the downstream path, i.e. sending a piece of
data. The data will be transported in the form of a packet. The first
thing that happens is that the packet is copied to the packet buffer
and ownership is transferred to Ouroboros. Then an FRCP header may be
added, the FRCP state machine will be updated (e.g. flow control
windows, next sequence number, last acknowledged sequence number etc),
and MAC/Encryption may be performed.

Now the packet is passed over the flow endpoint (the TX/RX FIFO's in
the figure) to the (unicast) IPCP.

The unicast IPCP implements a layer, and it reads packets coming from
flows allocated by the layer (or application) above -- referred to as
the (N+1)-flows -- and then forwards to other relaying IPCPs in the
layer, using the layer below (referred to as (N-1)-flows.

Now, remember the __qos parameter__? It not only enables or disables
functions related to FRCP or authentication/encryption, it also allows
some prioritization of packets. The IPCP has a two schedulers, one
that reads packets from the N+1 flows and another that reads packets
from N-1 flows.

Next it passes through congestion control. The DT protocol
(implemented in the Data Transfer Protocol Machine) has an ECN field
that is updated according to the _depth of the outgoing flow
queue_. The TX/RX queues between the layer keep track of how many
packets they have queued. If a packet is queued into a queue that has
a lot of packets, the ECN field is updated. This is adjustable per QoS
level. For instance, packets with a high QoS may get an ECN increase
of 1 and packets with low QoS may get an ECN increase of 8 if the
queue is quarter full. When a receiving IPCP sees high ECN values, it
will send a message to the sending IPCP. This scheme is commonly known
as Forward Excplicit Congestion Notification (FECN). Data Center TCP
also uses this approach. The congestion window operates in bytes
because network bandwidth is in bytes/s).

Finally, if the IPCP is receiving a lot of small packets, it will also
group them together into larger packets. We do this here (and not in
FRCP) because it's more efficient: the IPCP can group packets from
many different flows towards the same destination.

And then the cycle repeats: the packets are send according to the same
process to the layer below. One difference is that when an (N)-IPCP an
(N-1)-IPCP, it will avoids a copy, and only pass a reference to the
packet in the packet buffer.

While all these functions are potentially present in every layer, this
does not mean they must be present or enabled in every layer. Think of
Ouroboros layers as humans: all are equal, none are identical.

[^1]: Congestion control is completely decoupled and comes later.
[^2]: Encryption is implemented, authentication is pending.