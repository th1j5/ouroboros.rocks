---
title: "FAQ"
date:  2019-06-22
draft: false
description: >
    Frequently Asked Questions.
weight: 85
---

Got a question that is not listed here? Just pop it on our IRC channel
or mailing list and we will be happy to answer it!

[What is Ouroboros?](#what)\
[Is Ouroboros the same as the Recursive InterNetwork Architecture
(RINA)?](#rina)\
[How can I use Ouroboros right now?](#deploy)\
[What are the benefits of Ouroboros?](#benefits)\
[How do you manage the namespaces?](#namespaces)\

### <a name="what">What is Ouroboros?</a>

Ouroboros is a packet-based IPC mechanism. It allows programs to
communicate by sending messages, and provides a very simple API to do
so. At its core, it's an implementation of a recursive network
architecture. It can run next to, or over, common network technologies
such as Ethernet and IP.

[[back to top](#top)]

### <a name="rina">Is Ouroboros the same as the Recursive InterNetwork Architecture (RINA)?</a>

No. Ouroboros is a recursive network, and is born as part of our
research into RINA networks. Without the pioneering work of John Day and
others on RINA, Ouroboros would not exist. We consider the RINA model an
elegant way to think about distributed applications and networks.

However, there are major architectural differences between Ouroboros and
RINA. The most important difference is the location of the "transport
functions" which are related to connection management, such as
fragmentation, packet ordering and automated repeat request (ARQ). RINA
places these functions in special applications called IPCPs that form
layers known as Distributed IPC Facilities (DIFs) as part of a protocol
called EFCP. This allows a RINA DIF to provide an *IPC service* to the
layer on top.

Ouroboros has those functions in *every* application. The benefit of
this approach is that it is possible to multi-home applications in
different networks, and still have a reliable connection. It is also
more resilient since every connection is - at least in theory -
recoverable unless the application itself crashes. So, Ouroboros IPCPs
form a layer that only provides *IPC resources*. The application does
its connection management, which is implemented in the Ouroboros
library. This architectural difference impact the components and
protocols that underly the network, which are all different from RINA.

This change has a major impact on other components and protocols. We are
preparing a research paper on Ouroboros that will contain all these
details and more.

[[back to top](#top)]

### <a name="deploy">How can I use Ouroboros right now?</a>

At this point, Ouroboros is a useable prototype. You can use it to build
small deployments for personal use. There is no global Ouroboros network
yet.

[[back to top](#top)]

### <a name="benefits">What are the benefits of Ouroboros?</a>

We get this question a lot, and there is no single simple answer to
it.  Its benefits are those of a RINA network and more. In general, if
two systems provide the same service, simpler systems tend to be the
more robust and reliable ones. This is why we designed Ouroboros the
way we did. It has a bunch of small improvements over current networks
which may not look like anything game-changing by themselves, but do
add up. The reaction we usually get when demonstrating Ouroboros, is
that it makes everything really really easy.

Some benefits are improved anonymity as we do not send source addresses
in our data transfer packets. This also prevents all kinds of swerve and
amplification attacks. The packet structures are not fixed (as the
number of layers is not fixed), so there is no fast way to decode a
packet when captured "raw" on the wire. It also makes Deep Packet
Inspection harder to do. By attaching names to data transfer components
(so there can be multiple of these to form an "address"), we can
significantly reduce routing table sizes.

The API is very simple and universal, so we can run applications as
close to the hardware as possible to reduce latency. Currently it
requires quite some work from the application programmer to create
programs that run directly over Ethernet or over UDP or over TCP. With
the Ouroboros API, the application doesn't need to be changed. Even if
somebody comes up with a different transmission technology, the
application will never need to be modified to run over it.

Ouroboros also makes it easy to run different instances of the same
application on the same server and load-balance them. In IP networks
this requires at least some NAT trickery (since each application is tied
to an interface:port). For instance, it takes no effort at all to run
three different webserver implementations and load-balance flows between
them for resiliency and seamless attack mitigation.

The architecture still needs to be evaluated at scale. Ultimately, the
only way to get the numbers, are to get a large (pre-)production
deployment with real users.

[[back to top](#top)]

### <a name="namespaces">How do you manage the namespaces?</a>

Ouroboros uses names that are attached to programs and processes. The
layer API always uses hashes and the network maps hashes to addresses
for location. This function is similar to a DNS lookup. The current
implementation uses a DHT for that function in the ipcp-normal (the
ipcp-udp uses a DynDNS server, the eth-llc and eth-dix use a local
database with broadcast queries).

But this leaves the question how we assign names. Currently this is
ad-hoc, but eventually we will need an organized way for a global
namespace so that application names are unique. If we want to avoid a
central authority like ICANN, a distributed ledger would be a viable
technology to implement this, similar to, for instance, namecoin.
